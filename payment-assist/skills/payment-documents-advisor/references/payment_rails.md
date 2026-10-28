# Payment rails: what the user needs to know

## 1. Choosing the rail

| Situation | Usual rail |
| - | - |
| EUR payment between accounts in SEPA countries (EU/EEA, Switzerland, UK, Monaco, San Marino, Andorra, Vatican, Albania, Montenegro, North Macedonia, Moldova, Serbia and some others; check the EPC list) | SEPA Credit Transfer (SCT) or SEPA Instant (SCT Inst) |
| Non-EUR currency, or recipient bank outside SEPA | SWIFT (international wire) |
| Recipient bank in SEPA country but not a SEPA participant | SWIFT, or ask the recipient for another account |

The SEPA country list is maintained by the European Payments Council: https://www.europeanpaymentscouncil.eu/document-library/other/epc-list-sepa-scheme-countries

## 2. SEPA Credit Transfer (SCT)

- Currency: EUR only.
- Required fields: beneficiary name, beneficiary IBAN, amount, remittance information (payment description, up to 140 characters). BIC is not required for SEPA payments within the EEA.
- Execution time: by the end of the next business day under PSD2 (Directive (EU) 2015/2366, Art. 83).
- Fees: under Regulation (EU) 2021/1230, a cross-border EUR payment within the EU costs the same as a domestic one.
- Reversal: once executed, the payer cannot unilaterally recall it. A recall request depends on the recipient bank and the recipient's consent.

## 3. SEPA Instant Credit Transfer (SCT Inst)

- Funds arrive within about 10 seconds, 24/7/365.
- Under the Instant Payments Regulation (Regulation (EU) 2024/886), PSPs in the euro area that offer regular EUR transfers must also offer instant transfers at no higher price.
- Users can set their own limits for instant payments (per transaction or per day) in their banking app.
- **Instant payments are effectively irreversible.** This makes them the preferred tool of scammers; take extra care with new payees.

## 4. Verification of Payee (VoP) — SEPA only

Under Regulation (EU) 2024/886 (Art. 5c), before a euro credit transfer is authorised, the payer's bank must check whether the beneficiary name matches the IBAN and show the result. Applies in the euro area since 9 October 2025; PSPs in non-euro EU member states must comply by 9 July 2027.

| Result | Meaning | What to tell the user |
| - | - | - |
| Match | Name and IBAN match. | "The name matches the account." |
| Close match | Name is similar but not exact; the bank shows the actual name. | "Check for typos. If the name shown is not the person or company you intend to pay, stop." |
| No match | Name does not match the account. | "Do not proceed unless you have confirmed the details through a separate trusted channel. If you proceed, you accept the risk that the money goes to the wrong person and may not be recoverable." |
| Verification not possible | The check could not be performed. | "Double-check the details with the recipient through a separate trusted channel before sending." |

Proceeding after a mismatch warning shifts liability for a misdirected payment to the payer. VoP does not detect scams where the scammer controls an account in their own name; a full match does not prove the recipient is legitimate.

## 5. SWIFT (international wire)

- Currencies: any; common ones EUR, USD, GBP, CHF.
- Required fields: beneficiary name, beneficiary full address (street, building, postcode, city, country), account number or IBAN, beneficiary bank BIC (SWIFT code), amount and currency, payment details. Some countries require extra codes (e.g. purpose codes in the UAE, India, China; IFSC in India; routing number for US domestic accounts; CNAPS in China; INN/KPP for some former-USSR countries).
- Address: incomplete addresses are a frequent cause of delays and returns. The SWIFT network now uses ISO 20022 messages, and from November 2026 banks move to structured or hybrid postal addresses (town and country in separate fields), so provide the address in full and in separate parts.
- Intermediary (correspondent) banks: the payment may pass through one or more banks. Each may screen it and may deduct fees. Each may ask questions, which can add days.
- Fee options: OUR (sender pays all fees), SHA (shared, the most common), BEN (recipient pays). Under EU rules, only SHA is allowed for payments within the EEA in EEA currencies.
- Timing: usually 1 to 5 business days; longer when an intermediary bank asks for information.
- No VoP: SWIFT payments do not have Verification of Payee. The user must double-check the name, account and address themselves.
- Reversal: a recall (via the bank) is possible only with the recipient bank's cooperation and is not guaranteed.

## 6. Information accompanying transfers (Wire Transfer Regulation)

Regulation (EU) 2023/1113 requires the payer's bank to send the payer's name, account number and address (or official ID number, customer ID, or date and place of birth) and the payee's name and account number. Missing or inconsistent information can cause the payee's bank or an intermediary to suspend or reject the payment. Practical implication: the beneficiary name must be exact and complete.

## 7. Crypto-linked payments

- Payments to crypto exchanges from a bank account are bank transfers like any other, but many banks apply extra checks or limits.
- In the EU, crypto-asset service providers must be authorised under MiCA (Regulation (EU) 2023/1114). Check the ESMA register before paying a platform.
- Crypto transfers are irreversible and a common target for scams; never send to someone who contacted you first.

## 8. Cash

- Carrying EUR 10,000 or more in cash (or equivalent) into or out of the EU must be declared to customs (Regulation (EU) 2018/1672).
- From 10 July 2027, cash payments above EUR 10,000 for goods and services will be prohibited across the EU (Regulation (EU) 2024/1624, Art. 80); several member states already have lower national caps.
