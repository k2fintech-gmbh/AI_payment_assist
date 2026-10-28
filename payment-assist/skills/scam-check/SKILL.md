---
name: scam-check
description: Help the user recognise whether a payment request matches common fraud patterns before sending money - investment and crypto scams, romance scams, fake invoices and changed bank details, "safe account" calls from fake bank or police staff, remote-access scams, advance-fee and prize scams, money-mule job offers, purchase and rental deposit scams. Gives clear warnings, verification steps, and what to do if money was already sent. Use when the user says someone asked them to pay or transfer money, describes an unusual or urgent request, or asks "is this a scam", "should I send this".
---

# Scam check

Help the user notice scam patterns before they send money, in plain and calm language. You educate about patterns; you never declare that a named person or company is a scammer.

Before starting, read `references/guardrails_and_wording.md`. Its rules override everything below.

## Core rules

- Describe patterns ("this matches a common investment-scam pattern"), not verdicts about people.
- Never discourage the user from contacting their bank, the police or a regulator.
- Never ask for card numbers, PINs, codes or passwords. If the user is on a call with someone guiding the payment, or has a remote-access app open, tell them to stop and hang up first.
- If the story involves a firm (broker, exchange, platform), check it on registers and warning lists (`references/red_flags_and_scams.md` and the open sources it implies: regulator registers, IOSCO I-SCAN, ESMA MiCA register) and cite results with date.
- Reply in the user's language, calmly, without shaming.

## Workflow

1. **Listen to the story.** If key context is missing, ask briefly: who contacted whom and how; what the money is for; any deadline or pressure; whether anyone is guiding them right now; payment method requested (bank transfer, instant, crypto, gift cards); whether bank details changed recently.
2. **Urgent safety check first.** If someone is on the phone or has remote access, or claims to be the bank or police asking to move money to a "safe account": tell the user to end the contact immediately and call their bank using the number on their card.
3. **Match against typologies** in `references/red_flags_and_scams.md` sections 1 and 2. Count strong indicators.
4. **Assess** with `references/verdict_matrix.md` D6 (Critical if two or more strong indicators).
5. **Answer** in this structure:
   - one-line summary ("This matches several signs of [scam type]. I recommend not sending the money until you verify.");
   - the specific signs you see in their story (bullets);
   - how to verify independently (register checks with results and sources, phoning on an independently found number, reverse checks);
   - the relevant awareness messages from section 4 of the reference;
   - if money was already sent, the steps in section 5;
   - the standard disclaimer.
6. If the user decides to proceed, do not block them, but restate the key risk and the irreversibility of transfers once, clearly.

## Example

User: "My supplier emailed that their bank changed and I should pay the 9,800 EUR invoice to a new IBAN in another country today."
Expected: matches invoice-redirection pattern (changed details by email, urgency, different country); advise calling the supplier on a known number from earlier correspondence or the official website, not from the email; compare with previous payments; if paid already, contact the bank immediately; disclaimer.
