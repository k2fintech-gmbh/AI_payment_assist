---
name: country-risk-check
description: Explain what to expect when sending money from the EU to a specific country or receiving money from it - FATF black and grey lists, the EU list of high-risk third countries, EU sanctions regimes, the EU tax non-cooperative list, and practical consequences such as enhanced checks, delays, extra documents, intermediary bank issues or likely refusals. Use when the user asks "can I send money to [country]", "is [country] high-risk or sanctioned", "why is my payment to [country] delayed", or plans a payment involving a specific country.
---

# Country risk check

Tell the user, with sources and dates, how a country is classified on public lists and what this usually means in practice for a bank transfer from the EU.

Before starting, read `references/guardrails_and_wording.md`. Its rules override everything below.

## Core rules

- Verify the current list status live; if that fails, use `references/jurisdictions_snapshot.md` and say so, naming the snapshot date.
- Never suggest routing through another country, currency, crypto or third parties to get around restrictions.
- Do not give legal advice on whether a specific transaction is permitted under sanctions. Explain what the regime generally covers and that the bank (and, where relevant, the national competent authority issuing licences) decides.
- Reply in the user's language.

## Workflow

1. **Identify the countries involved**: recipient's country, recipient bank's country, any intermediary country, origin or destination of goods. Ask if unclear. Territories matter (e.g. Crimea or other non-government-controlled areas of Ukraine are treated differently from the rest of Ukraine).
2. **Check each country** against:
   - FATF black list and grey list;
   - EU list of high-risk third countries;
   - EU Sanctions Map (does a regime exist, what it covers: asset freezes only, sectoral, trade, financial services);
   - EU list of non-cooperative jurisdictions for tax purposes.
   Sources and URLs are in `references/open_sources.md` section 2 and the EU Sanctions Map in section 1.
3. **Assess** with `references/verdict_matrix.md` D2.
4. **Explain the practical consequences** using `references/jurisdictions_snapshot.md` section 5 and `references/payment_rails.md`: SEPA or SWIFT, whether many EU banks avoid the corridor, intermediary banks, typical questions and documents, timing.
5. **Answer** in this structure:
   - one-line summary (e.g. "Kenya: on the FATF grey list and the EU high-risk list; payments are possible but expect enhanced checks");
   - table: list, status, source and date;
   - what to expect and how to prepare (documents, timing, fee option, realistic alternatives such as asking the recipient for an account in their country's major bank, never workarounds);
   - the standard disclaimer.

## Example

User: "I need to pay a freelancer in Vietnam 2,500 USD."
Expected: Vietnam is on the FATF grey list and EU high-risk list (verify live); no comprehensive EU sanctions regime; explain enhanced due diligence: contract or invoice, relationship, possibly source of funds; SWIFT with full address and purpose; 2 to 5 days; disclaimer.
