#!/usr/bin/env python3
"""Sync shared files into skills, validate the plugin, and build zip packages.

Usage:
    python3 tools/build.py            # sync + validate + package into dist/
    python3 tools/build.py --check    # validate only; fail if generated files are out of sync
"""

import argparse
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHARED = ROOT / "shared"
SKILLS = ROOT / "skills"
DIST = ROOT / "dist"

AGENT_PLUGINS_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
PORTABLE_FIELDS = {"$schema", "name", "version", "description", "author", "homepage",
                   "repository", "license", "keywords", "extensions"}

ALL_REFS = [
    "guardrails_and_wording.md",
    "open_sources.md",
    "jurisdictions_snapshot.md",
    "payment_rails.md",
    "documents_matrix.md",
    "red_flags_and_scams.md",
    "verdict_matrix.md",
]

# Which shared files each skill receives. references/ and scripts/ in a skill
# are fully generated from this map.
SKILL_MAP = {
    "transfer-precheck": {"references": ALL_REFS, "scripts": ["validate_iban.py"]},
    "counterparty-check": {"references": ["guardrails_and_wording.md", "open_sources.md", "verdict_matrix.md"]},
    "country-risk-check": {"references": ["guardrails_and_wording.md", "open_sources.md",
                                          "jurisdictions_snapshot.md", "payment_rails.md", "verdict_matrix.md"]},
    "payment-documents-advisor": {"references": ["guardrails_and_wording.md", "documents_matrix.md", "payment_rails.md"]},
    "scam-check": {"references": ["guardrails_and_wording.md", "red_flags_and_scams.md", "open_sources.md",
                                  "verdict_matrix.md"]},
    "iban-bic-check": {"references": ["guardrails_and_wording.md", "payment_rails.md", "open_sources.md"],
                       "scripts": ["validate_iban.py"]},
}

PROVIDER_WORDS = re.compile(r"\b(claude|anthropic|chatgpt|openai|gpt-?\d*|codex|gemini)\b", re.IGNORECASE)
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
PLUGIN_NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9]|[-.](?=[a-z0-9]))*$")
FILE_REF_RE = re.compile(r"`((?:references|scripts|assets)/[A-Za-z0-9_.\-/]+)")
MAX_SKILL_LINES = 500
PACKAGE_ITEMS = ["plugin.json", ".claude-plugin", "skills"]


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)


def expected_files():
    """Map of generated file path -> source path."""
    files = {}
    for skill, kinds in SKILL_MAP.items():
        for kind, names in kinds.items():
            for name in names:
                files[SKILLS / skill / kind / name] = SHARED / kind / name
    return files


def sync(report, check_only):
    expected = expected_files()
    for skill, kinds in SKILL_MAP.items():
        for kind in ("references", "scripts"):
            target_dir = SKILLS / skill / kind
            wanted = {p for p in expected if p.parent == target_dir}
            if target_dir.exists():
                for existing in target_dir.iterdir():
                    if existing.name == "__pycache__":
                        continue
                    if existing not in wanted:
                        if check_only:
                            report.error(f"stale generated file: {existing.relative_to(ROOT)}")
                        else:
                            if existing.is_dir():
                                shutil.rmtree(existing)
                            else:
                                existing.unlink()
            if not wanted and target_dir.exists() and not check_only and not any(target_dir.iterdir()):
                target_dir.rmdir()

    for target, source in expected.items():
        if not source.exists():
            report.error(f"missing shared source: {source.relative_to(ROOT)}")
            continue
        if target.exists() and target.read_bytes() == source.read_bytes():
            continue
        if check_only:
            report.error(f"out of sync: {target.relative_to(ROOT)} (run tools/build.py)")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)


def parse_frontmatter(text):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    block = text[4:end]
    body = text[end + 4:]
    fields = {}
    for line in block.splitlines():
        if not line.strip():
            continue
        if ":" not in line or line.startswith((" ", "\t")):
            fields.setdefault("_unparsed", []).append(line)
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        quoted = len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'"
        if not quoted and (": " in value or " #" in value or value[:1] in "&*!|>%@`[{"):
            fields.setdefault("_unsafe", []).append(key.strip())
        fields[key.strip()] = value[1:-1] if quoted else value
    return fields, body


def validate_skill(skill_dir, report):
    rel = skill_dir.relative_to(ROOT)
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        report.error(f"{rel}: missing SKILL.md")
        return
    text = skill_md.read_text(encoding="utf-8")
    fields, body = parse_frontmatter(text)
    if fields is None:
        report.error(f"{rel}: SKILL.md must start with YAML frontmatter")
        return
    if "_unparsed" in fields:
        report.error(f"{rel}: frontmatter must use single-line 'key: value' entries")
    for key in fields.get("_unsafe", []):
        report.error(f"{rel}: frontmatter '{key}' is not valid as a plain YAML scalar; quote it")

    name = fields.get("name", "")
    description = fields.get("description", "")
    if not SKILL_NAME_RE.match(name) or len(name) > 64:
        report.error(f"{rel}: invalid name '{name}'")
    if name != skill_dir.name:
        report.error(f"{rel}: name '{name}' must match directory name")
    if re.search(r"anthropic|claude", name):
        report.error(f"{rel}: name contains a reserved word")
    if not description:
        report.error(f"{rel}: description is empty")
    if len(description) > 1024:
        report.error(f"{rel}: description is {len(description)} chars (max 1024)")
    if re.search(r"<[^>]+>", description):
        report.error(f"{rel}: description must not contain XML tags")

    lines = text.count("\n") + 1
    if lines > MAX_SKILL_LINES:
        report.warn(f"{rel}: SKILL.md has {lines} lines (recommended max {MAX_SKILL_LINES})")

    for ref in sorted(set(FILE_REF_RE.findall(body))):
        if not (skill_dir / ref).exists():
            report.error(f"{rel}: SKILL.md references missing file {ref}")

    for path in skill_dir.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".py", ".txt"} and "__pycache__" not in path.parts:
            for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                match = PROVIDER_WORDS.search(line)
                if match:
                    report.error(f"{path.relative_to(ROOT)}:{lineno}: provider-specific word '{match.group(0)}'")


def validate_manifests(report):
    portable_path = ROOT / "plugin.json"
    claude_path = ROOT / ".claude-plugin" / "plugin.json"
    manifests = {}
    for path in (portable_path, claude_path):
        try:
            manifests[path] = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            report.error(f"missing {path.relative_to(ROOT)}")
        except json.JSONDecodeError as exc:
            report.error(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
    if len(manifests) != 2:
        return None

    portable = manifests[portable_path]
    claude = manifests[claude_path]

    if portable.get("$schema") != AGENT_PLUGINS_SCHEMA:
        report.error("plugin.json: $schema must be the Agent Plugins 1.0.0 identifier")
    unknown = set(portable) - PORTABLE_FIELDS
    if unknown:
        report.error(f"plugin.json: fields not allowed by Agent Plugins 1.0: {sorted(unknown)}")
    name = portable.get("name", "")
    if not (1 <= len(name) <= 64) or not PLUGIN_NAME_RE.match(name):
        report.error(f"plugin.json: invalid plugin name '{name}'")
    author = portable.get("author", {})
    if set(author) - {"name", "email", "url"}:
        report.error("plugin.json: author may only contain name, email, url")

    for key in ("name", "version", "description"):
        if portable.get(key) != claude.get(key):
            report.error(f"manifests disagree on '{key}'")

    interface = portable.get("extensions", {}).get("com.openai", {}).get("interface", {})
    for key in ("displayName", "shortDescription", "longDescription", "developerName", "category",
                "privacyPolicyURL", "termsOfServiceURL"):
        if not interface.get(key):
            report.error(f"plugin.json: extensions.com.openai.interface.{key} is required")
    for key in ("websiteURL", "privacyPolicyURL", "termsOfServiceURL"):
        if "example.com" in str(interface.get(key, "")):
            report.warn(f"plugin.json: {key} is a placeholder; replace before submission")
    for text in [portable.get("description", "")] + [str(v) for v in interface.values()]:
        match = PROVIDER_WORDS.search(text)
        if match:
            report.error(f"plugin.json: provider-specific word '{match.group(0)}' in listing text")
    return portable


def validate_marketplaces(report, plugin_name):
    repo_root = ROOT.parent
    candidates = {
        repo_root / ".claude-plugin" / "marketplace.json": lambda entry: entry.get("source"),
        repo_root / ".agents" / "plugins" / "marketplace.json": lambda entry: entry.get("source", {}).get("path"),
    }
    for path, source_of in candidates.items():
        if not path.exists():
            continue
        rel = path.relative_to(repo_root)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            report.error(f"{rel}: invalid JSON: {exc}")
            continue
        entries = [p for p in data.get("plugins", []) if p.get("name") == plugin_name]
        if not entries:
            report.error(f"{rel}: no entry named '{plugin_name}'")
            continue
        source = source_of(entries[0]) or ""
        if not source.startswith("./") or ".." in source or (repo_root / source).resolve() != ROOT:
            report.error(f"{rel}: source '{source}' must be a ./ path from the repo root to {ROOT.name}")


def validate(report):
    portable = validate_manifests(report)
    if portable:
        validate_marketplaces(report, portable.get("name"))
    skill_dirs = sorted(p for p in SKILLS.iterdir() if p.is_dir())
    if not skill_dirs:
        report.error("no skills found")
    for skill_dir in skill_dirs:
        if skill_dir.name not in SKILL_MAP:
            report.warn(f"{skill_dir.name}: not in SKILL_MAP; shared files are not synced into it")
        validate_skill(skill_dir, report)
    for name in SKILL_MAP:
        if not (SKILLS / name).is_dir():
            report.error(f"SKILL_MAP lists '{name}' but skills/{name} does not exist")
    if (ROOT / "bin").exists():
        report.error("bin/ directory prevents installation in claude.ai chat and Cowork")
    return portable


def add_tree(zf, path, arcroot):
    if path.is_file():
        zf.write(path, arcroot / path.relative_to(path.parent))
        return
    for item in sorted(path.rglob("*")):
        if item.is_file() and "__pycache__" not in item.parts and item.suffix != ".pyc":
            zf.write(item, arcroot / item.relative_to(path.parent))


def package(portable):
    name = portable["name"]
    version = portable["version"]
    if DIST.exists():
        shutil.rmtree(DIST)
    (DIST / "skills").mkdir(parents=True)

    plugin_zip = DIST / f"{name}-{version}.zip"
    with zipfile.ZipFile(plugin_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for item in PACKAGE_ITEMS:
            add_tree(zf, ROOT / item, Path(name))

    for skill_dir in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        with zipfile.ZipFile(DIST / "skills" / f"{skill_dir.name}.zip", "w", zipfile.ZIP_DEFLATED) as zf:
            add_tree(zf, skill_dir, Path())

    return plugin_zip


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="validate only, do not write")
    args = parser.parse_args()

    report = Report()
    sync(report, check_only=args.check)
    portable = validate(report)

    for msg in report.warnings:
        print(f"WARNING: {msg}")
    for msg in report.errors:
        print(f"ERROR: {msg}")
    if report.errors:
        print(f"\nFAILED with {len(report.errors)} error(s)")
        return 1

    if args.check:
        print("OK: plugin is valid and generated files are in sync")
        return 0

    plugin_zip = package(portable)
    print(f"OK: built {plugin_zip.relative_to(ROOT)} and per-skill archives in dist/skills/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
