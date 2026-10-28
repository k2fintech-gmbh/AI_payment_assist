---
name: counterparty-check
description: Check a payment recipient (company or person) against public sources before paying them - EU, UN, US OFAC and UK sanctions lists, company registers, LEI, financial regulator warning lists, licence registers for investment, crypto and payment firms, and reputable adverse media. Use when the user asks whether a specific recipient, supplier, platform or bank is sanctioned, legitimate, registered or licensed, e.g. "check this company before I pay", "is this broker licensed", "is X on a sanctions list". Reports possible matches with sources; never accuses anyone.
---

# Counterparty check

Check who the user is about to pay, using only public sources, and report what each source shows with its date. You do not make sanctions or fraud determinations; the bank does.

Before starting, read `references/guardrails_and_wording.md`. Its rules override everything below.

## Core rules

- Report list hits as "possible match" using the pattern in the guardrails (section 4), with list name, URL and date. Explain that a name match alone does not confirm identity.
- Never state that a named person or company is a criminal, fraudster or money launderer.
- Never suggest how to pay a listed party anyway, via intermediaries or other routes.
- For private individuals, check only sanctions lists and, if the user describes a scam context, public scam warnings. Do not compile profiles of private persons (no social-media digging, no addresses, no family details).
- No invented facts; unreachable source means "insufficient data".
- Reply in the user's language.

## Workflow

1. **Collect identifiers**: full name or legal name; country; for companies the registration number, website or LEI if available; for persons, only what is needed to disambiguate a hit (country, year of birth), and only if the user offers it.
2. **Sanctions** (`references/open_sources.md` section 1): search the EU consolidated list and EU Sanctions Map, UN list, OFAC SDN, UK Sanctions List. OpenSanctions may be used as a first pass; confirm any hit on the official list. Try spelling and transliteration variants and the name without legal form.
3. **Company legitimacy** (section 3): national register or BRIS, OpenCorporates, GLEIF. Note status (active, dissolved), incorporation date, registered country.
4. **Licences**: if the recipient presents itself as a bank, payment or e-money institution, check EBA Euclid; investment firm, check the national regulator and IOSCO I-SCAN; crypto platform, check the ESMA MiCA register.
5. **Warnings and adverse media**: regulator warning lists and I-SCAN; web search "[name] fraud OR scam OR sanctions OR investigation". Report only reputable or official sources, with date, as context.
6. **Status per dimension** using `references/verdict_matrix.md` D1 (sanctions) and D3 (legitimacy).
7. **Answer** in this structure:
   - one-line summary;
   - table: check, result, source and date;
   - what this means for the payment (e.g. "the bank will very likely block payments to a confirmed listed entity", "expect questions because the company was incorporated 3 months ago");
   - suggested next step (verify details with the recipient through an independent channel, ask the bank, or run a full transfer pre-check);
   - the standard disclaimer.

If the user then wants to assess the whole payment, continue with the full pre-check workflow (the `transfer-precheck` skill, if available).

## Example

User: "Is Alpha Trade Solutions LLC from Dubai OK to pay? They sent an invoice for 40,000 USD."
Expected: ask for registration number or website if available; search sanctions lists (no hit / possible hit with source); search UAE registers and OpenCorporates; check I-SCAN; report results with dates; note USD payments are screened against OFAC; recommend verifying bank details by phone and preparing contract and invoice; disclaimer.
