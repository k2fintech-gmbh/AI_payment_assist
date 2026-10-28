# Open sources catalogue

Use web search to query these sources live. Always record for each source: what you searched, the result, and the date checked. If a source cannot be reached, say so and mark that check as "insufficient data" instead of guessing.

Search tips: try the name as entered, without legal-form suffixes (Ltd, GmbH, LLC, OOO), in Latin transliteration variants (e.g. Aleksandr / Alexander / Oleksandr), and with the country. For companies, also search the registration number if the user has it.

## 1. Sanctions lists

| Source | URL | Use for | Notes |
| - | - | - | - |
| EU Sanctions Map | https://www.sanctionsmap.eu | Country regimes, sectoral restrictions, listed persons per regime | Primary EU reference for "is there an EU regime for this country and what does it cover". |
| EU consolidated list of financial sanctions (FSF) | https://data.europa.eu/data/datasets/consolidated-list-of-persons-groups-and-entities-subject-to-eu-financial-sanctions | Persons and entities under EU asset freeze | Binding for EU persons and EU banks. |
| UN Security Council Consolidated List | https://main.un.org/securitycouncil/en/content/un-sc-consolidated-list | UN-designated persons and entities | Implemented in the EU by EU acts. |
| OFAC Sanctions List Search (US) | https://sanctionssearch.ofac.treas.gov | SDN and other US lists | Not directly binding on EU persons, but most banks with USD exposure apply it; USD payments are almost always screened against it. |
| UK Sanctions List (FCDO) | https://www.gov.uk/government/publications/the-uk-sanctions-list | UK designations | Relevant for GBP payments and UK banks in the chain. |
| OpenSanctions | https://www.opensanctions.org | Aggregated search across many lists, PEPs, debarment lists | Convenient first pass; confirm hits on the official list. |

## 2. Country risk lists

| Source | URL | Use for |
| - | - | - |
| FATF "black and grey" lists | https://www.fatf-gafi.org/en/countries/black-and-grey-lists.html | High-risk jurisdictions subject to a call for action (black list); jurisdictions under increased monitoring (grey list). Updated after each plenary (February, June, October). |
| EU list of high-risk third countries (Delegated Regulation (EU) 2016/1675, as amended) | https://finance.ec.europa.eu/financial-crime/anti-money-laundering-and-countering-financing-terrorism-international-level_en | Countries for which EU banks must apply enhanced due diligence. |
| EU list of non-cooperative jurisdictions for tax purposes | https://www.consilium.europa.eu/en/policies/eu-list-of-non-cooperative-jurisdictions/ | Tax-related risk factor; often triggers extra questions. |

## 3. Recipient legitimacy

| Source | URL | Use for |
| - | - | - |
| EU Business Registers search (BRIS, e-Justice) | https://e-justice.europa.eu/topics/registers-business-insolvency-land/business-registers-search-company-eu_en | Company exists in an EU/EEA register, status, registered address. |
| National business registers | Search "[country] company register" | Status, incorporation date, directors where public. |
| OpenCorporates | https://opencorporates.com | Cross-country company lookup. |
| GLEIF LEI search | https://search.gleif.org | Legal Entity Identifier, legal name, address, parent company. |
| EBA Euclid register (payment and e-money institutions) | https://euclid.eba.europa.eu/register/ | Whether a payment or e-money institution is authorised in the EU. |
| ESMA MiCA registers (crypto-asset service providers) | https://www.esma.europa.eu/esmas-activities/digital-finance-and-innovation/markets-crypto-assets-regulation-mica | Whether a crypto platform is an authorised CASP in the EU. |
| IOSCO I-SCAN | https://www.iosco.org/i-scan/ | Investor warnings from securities regulators worldwide. |
| National regulator warning lists | e.g. FCA Warning List https://www.fca.org.uk/scamsmart/warning-list ; BaFin, AMF, CONSOB, CNMV, MFSA, CySEC warning pages | Unauthorised firms and clone firms. |
| Adverse media | Web search: "[name]" + fraud / scam / sanctions / investigation / court | Only report results from reputable outlets or official sources, with date. Treat as context, never as proof. |

## 4. Bank and account details

| Source | URL | Use for |
| - | - | - |
| SWIFT IBAN Registry | https://www.swift.com/standards/data-standards/iban-international-bank-account-number | IBAN length and structure per country. |
| SWIFT BIC search | https://www2.swift.com/bsl/ | Whether a BIC exists and which institution it belongs to. |
| EPC register of SEPA scheme participants | https://www.europeanpaymentscouncil.eu/what-we-do/be-involved/register-participants | Whether the recipient bank participates in SEPA (SCT / SCT Inst). |
| ECB list of supervised entities | https://www.bankingsupervision.europa.eu/banking/list/html/index.en.html | Significant euro-area banks. |

The bundled script `scripts/validate_iban.py` checks IBAN checksum, country length and BIC format offline. It does not confirm that the account exists or who holds it.

## 5. Trade and goods

| Source | URL | Use for |
| - | - | - |
| EU dual-use export controls | https://policy.trade.ec.europa.eu/help-exporters-and-importers/exporting-dual-use-items_en | Whether goods may need an export licence (Regulation (EU) 2021/821). |
| EU Sanctions Map (sectoral) | https://www.sanctionsmap.eu | Import/export bans per country (e.g. Russia, Belarus, Iran, DPRK). |

## 6. How to report a source in the answer

Format each finding as:

- **[Check name]**: [result in one sentence]. Source: [name], [URL], checked [date].

If web search is not available in the current environment, tell the user at the start: "Live web search is not available, so I cannot check sanctions lists or registers right now. I can still help with documents, payment details and scam warnings." Mark all list-based dimensions as "insufficient data".
