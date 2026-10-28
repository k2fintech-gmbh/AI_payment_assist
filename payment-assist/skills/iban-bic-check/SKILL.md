---
name: iban-bic-check
description: Validate an IBAN and BIC/SWIFT code before a transfer - checksum, country-specific length, BIC format, consistency between IBAN country, BIC country and the recipient's declared country - and explain SEPA reachability, Verification of Payee (VoP) results, and which fields a SWIFT payment needs. Use when the user asks "is this IBAN correct", "which bank/country is this IBAN", "what does the VoP name mismatch mean", "what details do I need for an international transfer", or pastes account details to check.
---

# IBAN and BIC check

Check payment details structurally and explain what the bank's checks (VoP, SWIFT fields) mean for the user.

Before starting, read `references/guardrails_and_wording.md`. Its rules override everything below.

## Core rules

- A structurally valid IBAN does not prove the account exists or belongs to the intended recipient. Always say so.
- Never ask for card numbers, PINs, codes or passwords. The user may mask the middle of an IBAN only if they want general advice; the checksum then cannot be verified.
- Do not invent bank names. Identify the bank from the BIC or IBAN only if you can confirm it through a public source (SWIFT BIC search, the bank's website) and cite it; otherwise say you cannot confirm it.
- Reply in the user's language.

## Workflow

1. **Get the details**: IBAN or account number; BIC if available; the recipient's declared country; the rail if known.
2. **Run the script** (code execution):
   `python3 scripts/validate_iban.py --iban "<IBAN>" --bic "<BIC>" --country <ISO2>`
   If code execution is unavailable, perform the mod-97 check by careful reasoning and state that the result is less reliable.
3. **Interpret the output**:
   - checksum or length failure: likely typo; ask the user to re-check with the recipient (do not try to "fix" digits by guessing);
   - IBAN country differs from BIC country or from the declared country: explain this can be legitimate (e.g. payment institutions with foreign IBANs) but is also common in scams; suggest confirming with the recipient through a separate channel;
   - `sepa_country` true: SEPA likely possible for EUR; still confirm the bank participates (EPC register, `references/open_sources.md` section 4).
4. **Explain the rail-specific points** from `references/payment_rails.md`:
   - SEPA: VoP results (match, close match, no match, not possible) and what to do for each; liability shift if proceeding after a mismatch;
   - SWIFT: required fields (full structured address, BIC, country-specific codes), no VoP, intermediary fees and timing.
5. **Answer**: result line (valid / invalid with reason); details table (country, length, checksum, BIC parts, consistency warnings); what to do next; limitation note ("structural check only").

## Example

User: "My bank shows 'close match: Jon Smit Ltd' when I enter John Smith Ltd. Is that OK?"
Expected: explain close match: the bank sees a similar but not identical name; check for typos; if "Jon Smit Ltd" is not the company you intend to pay, stop and verify through a separate channel; proceeding after a warning shifts liability to you.
