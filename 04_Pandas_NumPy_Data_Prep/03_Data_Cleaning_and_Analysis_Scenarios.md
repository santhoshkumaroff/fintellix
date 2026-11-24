# Data Cleaning & Analysis – Scenario Questions

These are the "how would you..." questions where interviewers check your thinking, not just syntax. Use this structure: **Understand → Profile → Clean → Validate → Document**.

### Q1. You receive a loan file from a bank. What checks do you run first?
**Answer:**
1. **Structure:** expected columns present, row count vs control total.
2. **Types:** numbers numeric, dates parse.
3. **Completeness:** nulls in mandatory fields.
4. **Uniqueness:** duplicate loan_ids.
5. **Validity:** ranges (no negative balance, rate 0–36%, DPD ≥ 0), formats (PAN, IFSC).
6. **Consistency:** NPA flag agrees with DPD, closed loans have zero balance.
7. **Reconciliation:** totals match the GL or the source control report.
```python
checks = {
    "missing_cols": set(REQUIRED) - set(df.columns),
    "dup_ids": df["loan_id"].duplicated().sum(),
    "neg_balance": (df["outstanding"] < 0).sum(),
    "null_outstanding": df["outstanding"].isna().sum(),
    "bad_rate": (~df["interest_rate"].between(0, 36)).sum(),
}
```
- **Example 1:** The bank says 10,000 rows but the file has 9,998, so ask for the 2 missing rows before processing.
- **Example 2:** 40 loans have DPD > 90 but NPA flag = 'N', so raise a data-quality exception to the bank.

### Q2. How do you detect outliers?
**Answer:** Use the **IQR rule** (below Q1 − 1.5·IQR or above Q3 + 1.5·IQR), **z-score** (|z| > 3), percentiles, or business rules. In banking, an outlier may be real (a large corporate loan), so **flag it, don't delete it**.
```python
q1, q3 = df.outstanding.quantile([.25, .75]); iqr = q3 - q1
outliers = df[(df.outstanding < q1 - 1.5*iqr) | (df.outstanding > q3 + 1.5*iqr)]
```
- **Example 1:** A ₹500 crore personal loan is almost certainly a data entry error (an extra zeros problem).
- **Example 2:** A ₹500 crore corporate term loan is plausible, so verify it but keep it.

### Q3. How would you reconcile two datasets?
**Answer:** Match on keys with an outer merge, then classify the results: matched & equal, matched but different, only in A, only in B. Aggregate the differences.
```python
m = a.merge(b, on="account_id", how="outer", suffixes=("_src", "_rpt"), indicator=True)
m["diff"] = m["balance_src"].fillna(0) - m["balance_rpt"].fillna(0)
breaks = m[(m["_merge"] != "both") | (m["diff"].abs() > 1)]
```
- **Example 1:** Core banking vs reporting data: 3 accounts are missing in the report and 2 have rounding differences.
- **Example 2:** Comparing an LLM-extracted table from a PDF against the ground-truth Excel to measure extraction accuracy.

### Q4. Data is coming from 3 branches with different column names. How do you standardise?
**Answer:** Keep a **mapping config** (YAML or JSON) per source → standard schema, rename columns, cast types, and validate. Don't hard-code mappings in the logic.
```python
MAP = {"blr": {"Loan No": "loan_id", "O/S Amt": "outstanding"},
       "mum": {"LOAN_ID": "loan_id", "BAL": "outstanding"}}
frames = [pd.read_csv(f"{b}.csv").rename(columns=MAP[b]).assign(branch=b) for b in MAP]
std = pd.concat(frames, ignore_index=True)
```
- **Example 2:** An LLM can **suggest** the mapping for a new source ("O/S Amt" → outstanding). A human approves it and the result is saved to the config. This mirrors Fintellix's standard data model idea.

### Q5. How would you find the top 5 customers by total exposure?
```python
(df.groupby("customer_id")["outstanding"].sum()
   .nlargest(5).reset_index())
```
- **Example 2:** Customer C01 has a home loan plus a personal loan. Exposure must be summed at **customer** level, not per loan. This is a classic trap.

### Q6. How do you compute month-over-month NPA movement?
**Answer:** Compare snapshots: loans that became NPA this month (slippages), NPA loans that were upgraded or closed, and loans that stayed NPA.
```python
prev = prev_month.set_index("loan_id")["is_npa"]
curr = this_month.set_index("loan_id")["is_npa"]
joined = pd.concat([prev, curr], axis=1, keys=["prev", "curr"]).fillna(False)
fresh_npa = joined[(~joined.prev) & (joined.curr)].index
upgraded  = joined[(joined.prev) & (~joined.curr)].index
```
- **Example 1:** 25 new NPAs worth ₹12 cr in agri loans after a poor monsoon.
- **Example 2:** An LLM writes the commentary from these computed numbers (the numbers come from code, not the LLM).

### Q7. What is EDA and what do you look at?
**Answer:** Exploratory Data Analysis means understanding the data before modelling: shape, types, missing values, distributions (histograms), outliers (box plots), relationships (correlation, groupby), and class balance.
- **Example 1:** NPA is only 4% of loans, so a default model needs to handle class imbalance.
- **Example 2:** The interest rate distribution shows two peaks (secured vs unsecured loans).

### Q8. How do you split data for a model and avoid leakage?
**Answer:** Split train and test **before** fitting scalers or encoders. Fit on train only. For time-based data, split by time. Never use features that are only known after the outcome.
- **Example 1:** Predicting default with "recovery_amount" as a feature is leakage, because it's only known after default.
- **Example 2:** Train on 2022–2024 loans, test on 2025 loans.

### Q9. How do you encode categorical variables and scale numbers?
**Answer:** One-hot encoding for low-cardinality nominal features (`pd.get_dummies`), ordinal mapping for ordered ones, target or frequency encoding for high cardinality. Scale with StandardScaler or MinMaxScaler for distance-based models (tree models don't need scaling).
- **Example 1:** product → HOME/CAR/PERSONAL one-hot columns.
- **Example 2:** Rating grade AAA > AA > A → 3, 2, 1 ordinal.

### Q10. How do you prepare data for an LLM / RAG pipeline (vs a ML model)?
**Answer:** For RAG you prepare **documents**, not feature tables: extract text (PDF, HTML), clean it, split into chunks of roughly 300–800 tokens with overlap, attach metadata, embed, then store in a vector DB. For tabular data you either convert rows to text or use text-to-SQL.
- **Example 1:** 200 RBI circular PDFs → 6,000 chunks with `{circular_no, date, section}` metadata.
- **Example 2:** For questions over a loan table, don't embed rows. Let the LLM write SQL against the table (the Finbot approach).

### Q11. A report total suddenly dropped 30% this month. How do you investigate?
**Answer:** Check for **data issues first**: row counts vs last month, missing branches or products, a changed file format, duplicate removal, a filter or date bug. Then check **business reasons**: write-offs, a large repayment, a reclassification. Drill down by dimension (branch, product) to localise the drop.
- **Example 1:** The MUM branch file was empty because the extract job failed. That explains the drop.
- **Example 2:** A ₹2,000 cr corporate loan was repaid. That's genuine, and you document it in the commentary.

### Q12. How do you make a data pipeline reproducible and auditable?
**Answer:** Version the code (Git) and config, log row counts at every step, keep raw files immutable, write exception reports, make the pipeline idempotent (re-running gives the same result), and add tests.
- **Example 1:** Log lines like "raw=10,000 → after dedup=9,996 → after validation=9,950 (50 to exceptions)".
- **Example 2:** Each output carries `run_id`, `source_file_hash` and `code_version` columns.
