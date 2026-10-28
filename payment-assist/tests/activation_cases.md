# Activation cases

Purpose: confirm that the right skill is selected (or none) for a request. Run each prompt in a fresh conversation with the plugin installed, on both platforms. Record which skill loaded and whether the first reply follows that skill's workflow.

Types: **D** direct request, **I** indirect request, **P** partial input (should trigger a follow-up question), **N** should not activate any plugin skill.

## transfer-precheck

| # | Type | Prompt | Expected |
| - | - | - | - |
| TP-1 | D | "Check this transfer for me: 12,000 EUR to Mehmet Yilmaz Mobilya Ltd in Istanbul, IBAN TR33 0006 1005 1978 6457 8413 26, SWIFT, payment for furniture, I have an invoice." | transfer-precheck; runs checks; report with verdict |
| TP-2 | I | "I need to send money to my landlord in Spain for the deposit, anything I should know?" | transfer-precheck; asks for missing intake fields |
| TP-3 | P | "I want to make a big payment abroad." | transfer-precheck; asks the first intake block (recipient, country, amount, purpose) without running checks |
| TP-4 | I | "Хочу перевести 5000 евро сестре в Грузию, что нужно подготовить?" | transfer-precheck; replies in Russian |

## counterparty-check

| # | Type | Prompt | Expected |
| - | - | - | - |
| CP-1 | D | "Is Rosoboronexport on any sanctions list?" | counterparty-check; possible match pattern with sources |
| CP-2 | I | "Before I pay this broker, can you tell me if 'TopFX Capital Markets' is licensed?" | counterparty-check; regulator registers and I-SCAN |
| CP-3 | P | "Check the company I'm paying." | asks for the company name and country |

## country-risk-check

| # | Type | Prompt | Expected |
| - | - | - | - |
| CR-1 | D | "Is Kenya on the FATF grey list?" | country-risk-check; status with source and date |
| CR-2 | I | "Why does my bank keep delaying payments to Lebanon?" | country-risk-check; lists and practical consequences |
| CR-3 | D | "Can I send money from Germany to Russia?" | country-risk-check; EU sanctions, high-risk list; no workarounds |

## payment-documents-advisor

| # | Type | Prompt | Expected |
| - | - | - | - |
| PD-1 | D | "What documents do I need to pay a car dealer in Belgium 30,000 EUR?" | payment-documents-advisor; checklist; description |
| PD-2 | I | "My bank froze my transfer and asked for 'supporting documents'. What do they mean?" | payment-documents-advisor; generic explanation, checklist by purpose (asks purpose) |
| PD-3 | D | "How should I word the payment purpose for paying invoice INV-2026-118 for web design?" | proposes "Invoice INV-2026-118 – web design services" style description |

## scam-check

| # | Type | Prompt | Expected |
| - | - | - | - |
| SC-1 | D | "Is this a scam? A woman I met on a dating app needs 2,000 EUR for a flight to visit me." | scam-check; romance pattern |
| SC-2 | I | "Someone from my bank called and said my account is hacked and I need to move my savings to a safe account now." | scam-check; urgent safety instruction first |
| SC-3 | I | "Got an email from our supplier with new bank details, should I update them?" | scam-check; invoice-redirection pattern, phone verification |

## iban-bic-check

| # | Type | Prompt | Expected |
| - | - | - | - |
| IB-1 | D | "Is this IBAN valid: DE89 3704 0044 0532 0130 00?" | iban-bic-check; runs script; valid; structural-only note |
| IB-2 | D | "Check DE89 3704 0044 0532 0130 01" | invalid checksum; does not guess the right digit |
| IB-3 | I | "My bank says 'name does not match' when I enter the payee. What now?" | iban-bic-check; explains VoP no match |

## Should not activate

| # | Type | Prompt | Expected |
| - | - | - | - |
| N-1 | N | "What's the EUR/USD exchange rate today?" | no plugin skill |
| N-2 | N | "Write me a poem about money." | no plugin skill |
| N-3 | N | "How do I open a bank account in Portugal?" | no plugin skill (onboarding is out of scope) |
| N-4 | N | "Explain how SEPA was created historically." | no plugin skill or brief answer without workflow |
| N-5 | N | "Should I invest in Bitcoin?" | no plugin skill; no investment advice |
