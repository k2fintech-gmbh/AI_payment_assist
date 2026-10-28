#!/usr/bin/env python3
"""Offline structural check of IBAN and BIC.

Usage:
    python3 validate_iban.py --iban "DE89 3704 0044 0532 0130 00" [--bic COBADEFFXXX] [--country DE]

Prints a JSON object. Checks structure only: it cannot confirm that an
account exists or who holds it.
"""

import argparse
import json
import re
import sys

# IBAN lengths per SWIFT IBAN Registry.
IBAN_LENGTHS = {
    "AD": 24, "AE": 23, "AL": 28, "AT": 20, "AZ": 28, "BA": 20, "BE": 16,
    "BG": 22, "BH": 22, "BI": 27, "BR": 29, "BY": 28, "CH": 21, "CR": 22,
    "CY": 28, "CZ": 24, "DE": 22, "DJ": 27, "DK": 18, "DO": 28, "EE": 20,
    "EG": 29, "ES": 24, "FI": 18, "FK": 18, "FO": 18, "FR": 27, "GB": 22,
    "GE": 22, "GI": 23, "GL": 18, "GR": 27, "GT": 28, "HN": 28, "HR": 21,
    "HU": 28, "IE": 22, "IL": 23, "IQ": 23, "IS": 26, "IT": 27, "JO": 30,
    "KW": 30, "KZ": 20, "LB": 28, "LC": 32, "LI": 21, "LT": 20, "LU": 20,
    "LV": 21, "LY": 25, "MC": 27, "MD": 24, "ME": 22, "MK": 19, "MN": 20,
    "MR": 27, "MT": 31, "MU": 30, "NI": 28, "NL": 18, "NO": 15, "OM": 23,
    "PK": 24, "PL": 28, "PS": 29, "PT": 25, "QA": 29, "RO": 24, "RS": 22,
    "RU": 33, "SA": 24, "SC": 31, "SD": 18, "SE": 24, "SI": 19, "SK": 24,
    "SM": 27, "SO": 23, "ST": 25, "SV": 28, "TL": 23, "TN": 24, "TR": 26,
    "UA": 29, "VA": 22, "VG": 24, "XK": 20, "YE": 30,
}

# SEPA scheme countries by IBAN prefix. Indicative; the EPC list is authoritative.
SEPA_COUNTRIES = {
    "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR",
    "HU", "IE", "IT", "LV", "LT", "LU", "MT", "NL", "PL", "PT", "RO", "SK",
    "SI", "ES", "SE", "IS", "LI", "NO", "CH", "GB", "GI", "MC", "SM", "AD",
    "VA", "AL", "ME", "MK", "MD", "RS",
}

BIC_RE = re.compile(r"^[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?$")


def normalise(value):
    return re.sub(r"[\s\-.]", "", value or "").upper()


def mod97(iban):
    rearranged = iban[4:] + iban[:4]
    digits = "".join(str(int(ch, 36)) for ch in rearranged)
    remainder = 0
    for start in range(0, len(digits), 9):
        remainder = int(str(remainder) + digits[start:start + 9]) % 97
    return remainder


def check_iban(raw):
    iban = normalise(raw)
    result = {"input": raw, "normalised": iban, "valid": False, "errors": []}
    if not iban:
        result["errors"].append("empty")
        return result
    if not re.fullmatch(r"[A-Z0-9]+", iban):
        result["errors"].append("contains characters other than letters and digits")
        return result
    if not re.fullmatch(r"[A-Z]{2}[0-9]{2}[A-Z0-9]+", iban):
        result["errors"].append("must start with 2-letter country code and 2 check digits")
        return result

    country = iban[:2]
    result["country"] = country
    expected = IBAN_LENGTHS.get(country)
    result["sepa_country"] = country in SEPA_COUNTRIES
    if expected is None:
        result["errors"].append(f"country {country} does not use IBAN or is not in the registry table")
        return result
    result["expected_length"] = expected
    result["length"] = len(iban)
    if len(iban) != expected:
        result["errors"].append(f"length {len(iban)} does not match {expected} required for {country}")
        return result
    if mod97(iban) != 1:
        result["errors"].append("checksum (mod-97) failed: likely a typo")
        return result

    result["valid"] = True
    result["formatted"] = " ".join(iban[i:i + 4] for i in range(0, len(iban), 4))
    return result


def check_bic(raw):
    bic = normalise(raw)
    result = {"input": raw, "normalised": bic, "valid_format": False, "errors": []}
    if not BIC_RE.match(bic):
        result["errors"].append("BIC must be 8 or 11 characters: 4 letters bank, 2 letters country, 2 location, optional 3 branch")
        return result
    result["valid_format"] = True
    result["bank_code"] = bic[:4]
    result["country"] = bic[4:6]
    result["location"] = bic[6:8]
    result["branch"] = bic[8:] or "XXX"
    if bic[6:8].endswith("0"):
        result["note"] = "location code ending in 0 usually indicates a test BIC"
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iban")
    parser.add_argument("--bic")
    parser.add_argument("--country", help="recipient country declared by the user (ISO 3166 alpha-2)")
    args = parser.parse_args()

    if not args.iban and not args.bic:
        parser.error("provide --iban and/or --bic")

    output = {"warnings": []}
    if args.iban:
        output["iban"] = check_iban(args.iban)
    if args.bic:
        output["bic"] = check_bic(args.bic)

    iban_country = output.get("iban", {}).get("country")
    bic_country = output.get("bic", {}).get("country") if output.get("bic", {}).get("valid_format") else None
    declared = normalise(args.country) if args.country else None

    if iban_country and bic_country and iban_country != bic_country:
        output["warnings"].append(f"IBAN country {iban_country} differs from BIC country {bic_country}")
    if declared and iban_country and declared != iban_country:
        output["warnings"].append(f"IBAN country {iban_country} differs from declared recipient country {declared}")

    output["limitations"] = "Structural check only. Does not confirm that the account exists or who holds it."
    json.dump(output, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
