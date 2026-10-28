# Verdict matrix

The verdict is derived deterministically from dimension statuses. Do not override it with an overall impression. Assess each dimension first, then apply the resolution rules in order.

## 1. Dimension statuses

Each dimension gets exactly one status:

- **Clear**: checked against the relevant sources, nothing found.
- **Attention**: something the user should address or expect questions about.
- **Critical**: the payment is very likely to be blocked, prohibited, or the user is very likely being defrauded.
- **Unknown**: could not be checked (no data from the user, source unavailable, web search unavailable).

## 2. Dimensions and criteria

### D1. Sanctions (recipient, recipient bank, beneficial owner if known)

| Status | Criteria |
| - | - |
| Critical | Name plus at least one other identifier (country, date of birth, registration number, address, alias) matches an entry on the EU or UN list; or the recipient bank is under an EU asset freeze or transaction ban; or the payment falls under a clear EU prohibition for that country. |
| Attention | Name-only or partial match on any list; match only on OFAC or UK list; recipient connected to a country with broad EU restrictive measures without a confirmed listing. |
| Clear | No match on EU, UN, OFAC, UK lists (or OpenSanctions confirmed against official lists) on the date checked. |
| Unknown | Recipient name not provided, or lists could not be searched. |

### D2. Geography (recipient country, recipient bank country, any intermediary country, origin of goods)

| Status | Criteria |
| - | - |
| Critical | Any country on the FATF black list; or a country or territory subject to near-total EU restrictions (e.g. DPRK, non-government-controlled territories of Ukraine). |
| Attention | FATF grey list; EU high-risk third-country list; EU tax non-cooperative list; country with EU sectoral sanctions (e.g. Russia, Belarus); active conflict zone; account country differs from the recipient's declared country without explanation. |
| Clear | None of the above. |
| Unknown | Countries not provided. |

### D3. Recipient legitimacy

| Status | Criteria |
| - | - |
| Critical | Recipient (same name and website/registration) appears on a regulator warning list or IOSCO I-SCAN; company is dissolved or struck off; recipient claims to be a regulated investment or crypto firm but is not on the relevant register. |
| Attention | Company not found in any register; incorporated less than about 12 months ago for a large or unusual payment; payment for business purpose to a private person's account; credible adverse media; recipient is a payment or e-money institution acting as intermediary for an unknown end beneficiary. |
| Clear | Found active in an official register (or a natural person with a clear, explained relationship). |
| Unknown | Not enough identifying information. |

### D4. Payment details (technical)

| Status | Criteria |
| - | - |
| Attention | IBAN fails checksum or country length (must be fixed before sending); BIC format invalid or does not exist; IBAN country differs from declared recipient country; required SWIFT fields missing (address, purpose code where required); recipient bank not a SEPA participant for a SEPA payment. |
| Clear | IBAN and BIC structurally valid and consistent with the declared countries. |
| Unknown | No IBAN/BIC provided. |

D4 never produces Critical by itself: technical errors cause rejection or delay, not prohibition.

### D5. Purpose and documents

| Status | Criteria |
| - | - |
| Critical | The user asks to describe the payment as something other than its real purpose, or to hide the real recipient (also a guardrail breach: decline that part). |
| Attention | Purpose vague; purpose inconsistent with the relationship or with the user's stated activity; documents likely to be requested are not available; third-party payment; large gift or loan without documentation. |
| Clear | Purpose specific and consistent; relevant documents available. |
| Unknown | Purpose not stated. |

### D6. Fraud and scam indicators

| Status | Criteria |
| - | - |
| Critical | Two or more strong indicators from `red_flags_and_scams.md` (e.g. unsolicited contact plus guaranteed returns; "safe account" request; bank details changed by email plus urgency; remote-access tool in use; payment to "unlock" withdrawals). |
| Attention | One indicator; or new payee plus instant payment plus high amount relative to what the user describes as usual. |
| Clear | No indicators in what the user described. |
| Unknown | Context not provided (do not treat as Clear if the user refused to say how they met the recipient). |

### D7. Hard-stop topic

Any hard-stop topic from `guardrails_and_wording.md` section 3 stops the assessment immediately with the neutral refusal. No verdict is issued.

## 3. Resolution rules (apply in order)

1. D7 triggered: neutral refusal, no report.
2. Any dimension Critical: **RED — high risk / likely blocked**.
3. D1 or D2 Unknown: **GREY — insufficient data**. Explain what is missing and how to provide it. Sanctions and geography must never be assumed clear.
4. Any dimension Attention: **YELLOW — proceed with care**.
5. D3, D5 or D6 Unknown with everything else Clear: **YELLOW — proceed with care**, noting what was not assessed.
6. Otherwise: **GREEN — no issues found in open sources**.

## 4. Verdict labels for the user (translate)

| Verdict | Label | One-line meaning |
| - | - | - |
| GREEN | No issues found | No issues found in the open sources checked. Standard bank checks will still apply. |
| YELLOW | Proceed with care | The payment may be possible, but expect questions or delays, or fix the points listed first. |
| RED | High risk | The payment is very likely to be blocked or you may be at risk of fraud. Do not send until the points listed are resolved with your bank. |
| GREY | Insufficient data | Key checks could not be completed. Provide the missing information or check with your bank. |

The verdict is never "approved" or "safe".
