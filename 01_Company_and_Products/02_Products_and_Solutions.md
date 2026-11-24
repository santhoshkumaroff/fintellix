# Fintellix Products, Solutions & Data Flow

## 1. Platforms
| Platform | What it does | Simple example |
|---|---|---|
| **Data Curation Platform** | Codeless, self-service data curation. Delivers "curated, attested & trusted data" for business use | A finance user maps the core banking "loan_amt" field to the standard "outstanding_balance" without writing code |
| **Data Analytics Platform** | Builds data-driven applications and analytics on the curated data | A dashboard of NPA trend by branch |

## 2. Solutions
| Solution | Purpose |
|---|---|
| **Regulatory Reporting (RegTech)** | "Codeless" conversion from a standardised data schema to multiple regulatory formats (XBRL, XML, CSV, TXT, XLSX) |
| **Credit Risk** | NPA management, Early Warning System (EWS), Expected Credit Loss (ECL) |
| **Syndicate Reporting** | Pre-configured solution to generate, validate and report Lloyd's returns |
| **Supervisory Reporting (SupTech)** | Data collection and insights platform for regulators |
| **Finbot** | Conversational AI chatbot that gives data insights through SQL queries |
| **Compliance Tracker** | AI-driven regulatory change management and compliance tracking |
| **Adhoc Reporting** | Custom regulatory and management reports |

## 3. Countries / regulators (from fintellix.com)
| Country | Offering |
|---|---|
| India | RBI reporting, loan loss calculation, Risk-Based Supervision (RBS), ADEPT, fraud analytics, liquidity reporting, complaints management |
| UAE | CBUAE reporting |
| Saudi Arabia | SAMA reporting (incl. Shari'ah-compliant product categorisation) |
| Kuwait | CBK reporting, IFRS and risk |
| Mauritius | BoM reporting |
| Singapore | MAS reporting |
| Hong Kong | HKMA reporting |
| Australia | APRA and LCR reporting |
| South Korea | FCS reporting |
| Philippines | Data lake & analytics |
| Thailand | Data governance & MIS |
| UK | MIS & regulatory reporting, supervisory platform for insurance |
| USA | CECL & CCAR |

## 4. Features from the Bank of Mauritius solution sheet (2026)
- Pre-configured regulator templates
- Comprehensive **data model** covering the required subject areas
- **Validation framework**: built-in rules, consistency checks
- **Centralised rule engine** for metric computation
- **Data lineage & traceability**: drill down from the reported number to the granular loan/account rows
- **Business configuration UI**: manage taxonomies, one unified data version across reports
- **Workflow**: configurable multi-level **maker-checker** review and approval with audit trail
- Described as a **BCBS 239-compliant** data platform

## 5. The end-to-end data flow (draw this on the whiteboard if asked)

```
Source systems            Staging / Integration        Standard Data Model         Rule Engine            Output
(Core Banking: Finacle,   ---> (extract, load raw, ---> (loans, deposits,     ---> (validations,     ---> Regulator template
 Flexcube; Treasury;            basic checks)            customers, GL,             computations,          (XBRL / XML / CSV)
 Loan origination; GL)                                   collateral...)             mappings)              -> maker-checker
                                                                                                          -> submission (e.g. RBI CIMS)
                                            <---- Data lineage: drill-down from any reported cell back to rows ---->
```

### Where GenAI fits in this flow (talk about this in the interview)
| Stage | GenAI / Python use case |
|---|---|
| Regulation intake | Summarise new circulars, extract changed fields, Q&A over the rulebook (RAG) |
| Mapping | Suggest mappings from a bank's source column names to the standard data model ("cust_nm" → customer_name) |
| Validation | Explain *why* a validation failed in plain English for business users |
| Querying | Text-to-SQL (Finbot) so users can ask questions without SQL |
| Implementation | Auto-generate test cases, documentation and reconciliation scripts |
| Review | Draft commentary on report variances ("NPA rose 12% because of 3 large accounts in the agri segment") |

---

## Interview questions

### Q1. What does "codeless conversion from a standardised data schema to multiple regulatory formats" mean?
**Answer:** The bank's data is loaded **once** into a standard data model. Each regulator's template is defined as **configuration** (mappings, filters, aggregations), not hard-coded programs. So supporting a new report, or a change to an existing one, means changing configuration.
- **Example 1:** The same loan table feeds both RBI's NPA return and the bank's internal MIS. Only the template config differs.
- **Example 2:** RBI adds a new column "loan purpose" to a return. The analyst adds a mapping in the UI and no developer release is needed.

### Q2. What is data lineage and why do regulators care?
**Answer:** Lineage is the ability to trace a reported number back to its source rows and the rules applied to it. Regulators and auditors ask "where did this number come from?" Without lineage, the bank cannot defend its figures.
- **Example 1:** RBI questions a gross NPA figure of ₹520 crore. With lineage, the bank drills down to the 1,240 accounts and the 90-day overdue rule.
- **Example 2:** In a Python pipeline, you keep `source_file`, `row_id` and `rule_applied` columns, so any output row can be traced back.

### Q3. What is maker-checker?
**Answer:** A four-eyes control: one person (maker) prepares or changes data, and a different person (checker) reviews and approves it before it takes effect. It prevents errors and fraud. Fintellix's workflow supports configurable multi-level maker-checker with an audit trail.
- **Example 1:** An analyst adjusts a provision value (maker). The finance manager approves it (checker) before submission.
- **Example 2:** In Git, a developer raises a pull request (maker) and a reviewer approves it (checker) before merge. Same idea.

### Q4. What output formats do regulators accept?
**Answer:** XBRL (eXtensible Business Reporting Language, an XML-based standard for business data), XML, CSV, TXT, XLSX. RBI moved from XBRL to its CIMS data warehouse for many returns.
- **Example 1:** A balance sheet return in XBRL, where every number is tagged with a concept like "TotalDeposits."
- **Example 2:** A CSV file of large borrower exposures uploaded to a regulator portal.

### Q5. How could you use GenAI on Fintellix's products? (very likely question)
**Answer:** Pick 2–3 from the table above and explain one in depth with accuracy controls.
- **Example 1, circular Q&A:** RAG over RBI master directions. A user asks "What is the SMA-2 bucket?" The bot retrieves the paragraph, answers, and cites the circular number. I'd measure accuracy on 50 golden questions.
- **Example 2, mapping assistant:** Given a bank's 300 source column names and sample values, the LLM suggests the matching standard field with a confidence score. A human approves each suggestion (maker-checker), and accepted mappings become future few-shot examples.

### Q6. What would worry you about using an LLM in regulatory reporting?
**Answer:** Hallucination (made-up numbers), lack of explainability, data privacy (customer data must not leak), non-determinism, and audit. Mitigations: LLMs **never compute the reported numbers**, the rule engine does. LLMs assist with text, mapping and queries. Ground every answer with RAG and citations. Keep a human in the loop. Log prompts and outputs. Mask PII. Evaluate against test sets.
- **Example 1:** The LLM drafts variance commentary, but the numbers in it are injected from the database, not generated.
- **Example 2:** Text-to-SQL runs on a read-only replica with only SELECT permissions, and the SQL is shown to the user.
