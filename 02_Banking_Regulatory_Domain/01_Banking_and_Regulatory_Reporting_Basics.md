# Banking & Regulatory Reporting – What an Intern Must Know

> Nobody expects an intern to be a banker. They do expect you to know the basic vocabulary and show curiosity. Know these terms well enough to explain each in one line with an example.

---

### Q1. What is regulatory reporting?
**Answer:** Banks must regularly send data (returns) to their regulator, such as RBI in India: balance sheets, loans, NPAs, liquidity, capital, large exposures, frauds. The regulator uses it to supervise the bank's health and the system's stability. Reports have fixed formats, frequencies (daily, weekly, monthly, quarterly) and validation rules.
- **Example 1:** Every month a bank reports its NPAs to RBI.
- **Example 2:** Every fortnight banks report their liabilities so RBI can check they are holding enough CRR.

### Q2. What is RBI and what does it do?
**Answer:** The Reserve Bank of India is India's central bank. It issues currency, sets monetary policy (repo rate), regulates and supervises banks and NBFCs, and manages forex. Regulations come as **circulars** and **Master Directions**.
- **Example 1:** RBI changes the repo rate, which affects your home-loan EMI.
- **Example 2:** RBI issues a Master Direction on how banks must classify and provide for bad loans.

### Q3. What is an NPA?
**Answer:** A Non-Performing Asset is a loan where interest or principal has stayed **overdue for more than 90 days** (for most term loans). NPAs are sub-classified by age: **Substandard** (NPA ≤ 12 months), **Doubtful** (> 12 months), **Loss** (identified as uncollectible). Banks must keep **provisions** (money set aside) against them.
- **Example 1:** Ravi's car-loan EMI was due on 1 Jan and is still unpaid on 2 April (91 days). The loan becomes an NPA.
- **Example 2:** In pandas: `df["is_npa"] = df["days_past_due"] > 90`.

### Q4. What is SMA (Special Mention Account)?
**Answer:** An early-warning bucket before NPA: **SMA-0** = 1–30 days overdue, **SMA-1** = 31–60, **SMA-2** = 61–90. It helps banks act early. (Fintellix's Early Warning System works in this space.)
- **Example 1:** A loan 45 days overdue is SMA-1, so the bank calls the borrower.
- **Example 2:** `pd.cut(df.dpd, bins=[-1, 0, 30, 60, 90, np.inf], labels=["Standard","SMA-0","SMA-1","SMA-2","NPA"])`. Bins are right-inclusive, so 0 → Standard, 30 → SMA-0, 90 → SMA-2, 91 → NPA. Always test the boundary values.

### Q5. What are Gross NPA and Net NPA?
**Answer:** **Gross NPA** = total NPA loans. **Net NPA** = Gross NPA − provisions held. Both are often shown as a % of total advances.
- **Example 1:** Advances ₹10,000 cr, Gross NPA ₹500 cr → GNPA 5%. Provisions ₹300 cr → Net NPA ₹200 cr.
- **Example 2:** A dashboard tracking GNPA% month on month across branches.

### Q6. What is provisioning? What is PCR?
**Answer:** A provision is money set aside from profit to cover expected loan losses. **Provision Coverage Ratio (PCR)** = Provisions ÷ Gross NPA. A higher PCR means a better cushion.
- **Example:** Provisions ₹300 cr on GNPA ₹500 cr → PCR 60%.

### Q7. What is ECL (Expected Credit Loss)?
**Answer:** A forward-looking provisioning approach (IFRS 9 / Ind AS 109): provide for losses you **expect**, not only losses that have already happened. **ECL = PD × LGD × EAD**.
- **PD** (Probability of Default): chance the borrower defaults
- **LGD** (Loss Given Default): % lost if they default, after recovering collateral
- **EAD** (Exposure at Default): amount outstanding when they default
- Stages: **Stage 1** (performing → 12-month ECL), **Stage 2** (significant increase in credit risk → lifetime ECL), **Stage 3** (credit-impaired → lifetime ECL)
- **Example 1:** EAD ₹10 lakh, PD 2%, LGD 40% → ECL = 10,00,000 × 0.02 × 0.40 = ₹8,000.
- **Example 2:** A loan moves from Stage 1 to Stage 2 when it becomes 30+ days overdue, so its provision jumps from 12-month to lifetime ECL.
- **Tip:** Indian banks have historically used the "incurred loss" model. RBI has been moving banks towards ECL-based provisioning, so check the latest RBI direction and its effective date before the interview. Fintellix has an ECL engine.

### Q8. What is Basel III? What is CRAR / CAR?
**Answer:** Basel III is the international framework (from the Basel Committee on Banking Supervision, BCBS) for bank capital, liquidity and leverage. **Capital to Risk-weighted Assets Ratio (CRAR)** = Capital ÷ Risk-Weighted Assets. Basel requires a minimum of 8%. RBI requires a higher minimum (9%) plus a capital conservation buffer.
- **Example 1:** A home loan carries a lower risk weight than an unsecured personal loan, so it needs less capital.
- **Example 2:** A bank with ₹1,200 cr capital and ₹10,000 cr RWA has CRAR 12%.

### Q9. What is LCR? NSFR?
**Answer:** **Liquidity Coverage Ratio** = High-Quality Liquid Assets ÷ net cash outflows over the next 30 days under stress. It must be ≥ 100%. **Net Stable Funding Ratio** = available stable funding ÷ required stable funding, also ≥ 100% (a 1-year horizon). Fintellix offers LCR reporting for APRA (Australia).
- **Example:** A bank holds ₹1,100 cr of government bonds (HQLA) and expects ₹1,000 cr net outflows → LCR 110%.

### Q10. What are CRR and SLR?
**Answer:** **Cash Reserve Ratio:** % of deposits (NDTL) a bank must keep as cash with RBI. **Statutory Liquidity Ratio:** % of NDTL a bank must hold in liquid assets such as government securities. RBI sets both and changes them; quote current values only after checking RBI's site.
- **Example:** If CRR is 4% and a bank has ₹1,000 cr NDTL, it keeps ₹40 cr with RBI.

### Q11. What is BCBS 239?
**Answer:** Basel Committee principles (2013) for **risk data aggregation and risk reporting**: banks must produce accurate, complete, timely, adaptable risk data with clear governance and data ownership. Fintellix describes its platform as BCBS 239-compliant.
- **Example 1:** In a crisis, the CRO should get total exposure to one group of companies across all branches in hours, not weeks.
- **Example 2:** Every data element has a named owner and automated quality checks: the same discipline you apply in a data pipeline.

### Q12. What is XBRL? What is RBI CIMS?
**Answer:** **XBRL** is an XML-based standard in which every reported value is tagged with a defined concept from a taxonomy, so machines can read it. RBI mandated XBRL for online returns from 2012. **CIMS (Centralised Information Management System)** is RBI's next-generation data warehouse. RBI is moving many returns from the XBRL portal to CIMS, starting with commercial banks and extending to UCBs and NBFCs.
- **Example 1:** `<TotalDeposits contextRef="Q3FY26" unitRef="INR">5000000000</TotalDeposits>`.
- **Example 2:** Statutory returns Form A, Form VIII and Form IX were shifted to the CIMS portal.

### Q13. What is Risk-Based Supervision (RBS)?
**Answer:** The regulator focuses supervisory effort on banks and areas with higher risk, using data-driven risk scores instead of the same checks for everyone. Banks submit granular data for it. Fintellix lists RBS as an India solution.
- **Example:** A bank with rising NPAs and falling capital gets more frequent RBI scrutiny.

### Q14. What is a Core Banking System (CBS)?
**Answer:** The bank's central system that records accounts, deposits, loans and transactions in real time across branches. Common products are Infosys Finacle, Oracle Flexcube and TCS BaNCS. It is the main **source system** for regulatory reporting.
- **Example 1:** When you deposit cash at any branch, the CBS updates your balance instantly.
- **Example 2:** Fintellix extracts loan-level data from the CBS into its data model.

### Q15. What is a General Ledger (GL) and GL reconciliation?
**Answer:** The GL is the bank's accounting book of all balances. Reconciliation checks that the totals in the reporting data match the GL. If loan-level data adds up to ₹9,990 cr but the GL says ₹10,000 cr, the ₹10 cr gap must be explained before submission.
- **Example 1:** A Python script groups loan data by product and compares it to GL balances, flagging differences above ₹1 lakh.
- **Example 2:** Missing accounts in the extract are a common cause of reconciliation breaks.

### Q16. What are KYC and AML?
**Answer:** **KYC (Know Your Customer):** verify customer identity. **AML (Anti-Money Laundering):** detect and report suspicious transactions. Both are compliance requirements.
- **Example 1:** Asking for PAN and Aadhaar before opening an account.
- **Example 2:** Flagging 15 cash deposits of ₹49,000 each in a week (structuring to stay under a threshold).

### Q17. What is fraud reporting / fraud analytics?
**Answer:** Banks must report frauds to the regulator within set timelines. Analytics detects patterns such as unusual transaction velocity or mismatched device and location. Fintellix lists fraud analytics for India.
- **Example:** A card used in Bengaluru and Dubai 20 minutes apart.

### Q18. What is IFRS 9 / Ind AS 109? CECL? CCAR?
**Answer:** **IFRS 9** (international) / **Ind AS 109** (Indian equivalent) is the accounting standard for financial instruments, including ECL. **CECL** is the US equivalent: lifetime expected loss from day 1. **CCAR** is the US Fed's annual stress test of large banks' capital plans. Fintellix offers CECL and CCAR solutions for the USA.

### Q19. What does "granular data" mean in regulatory reporting?
**Answer:** Regulators increasingly ask for **account- or transaction-level** data instead of summary totals, so they can slice it themselves. This multiplies data volume and quality demands.
- **Example:** Instead of "total agri loans = ₹2,000 cr", the bank sends all 4 lakh agri loans with borrower type, district, interest rate and DPD.

### Q20. Why is data quality critical in banking?
**Answer:** Wrong data leads to wrong regulatory numbers, which brings penalties, reputational damage and bad decisions. Data quality dimensions: **completeness, accuracy, consistency, timeliness, validity, uniqueness**.
- **Example 1, validity:** A loan with a negative outstanding balance.
- **Example 2, uniqueness:** The same customer appearing under two customer IDs inflates the count of borrowers.

---

## Glossary for quick recall
| Term | One-liner |
|---|---|
| Advances | Loans given by the bank |
| NDTL | Net Demand and Time Liabilities (basically deposits) |
| DPD | Days Past Due |
| HQLA | High-Quality Liquid Assets |
| RWA | Risk-Weighted Assets |
| Exposure | Total amount a bank can lose on a borrower |
| Collateral | Asset pledged against a loan (house, gold) |
| Write-off | Removing a bad loan from the books after full provisioning |
| Restructuring | Changing loan terms to help a stressed borrower |
| Islamic banking | Shari'ah-compliant products (no interest; profit-sharing). Fintellix handles these for SAMA |
| Lloyd's | London insurance market; syndicates report to Lloyd's |
