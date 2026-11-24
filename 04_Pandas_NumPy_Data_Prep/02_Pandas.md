# Pandas (JD: "Pandas" + "Clean, analyse, and prepare data for models, reports, and Gen AI pipelines")

> Practise everything here on a small loans CSV. Sample data to paste into `loans.csv`:
```
loan_id,customer_id,branch,product,sanction_date,outstanding,dpd,interest_rate
L001,C01,BLR,HOME,2022-04-01,2500000,0,8.5
L002,C02,MUM,CAR,2023-01-15,600000,45,9.2
L003,C01,BLR,PERSONAL,2024-06-10,200000,120,14.0
L004,C03,DEL,HOME,2021-11-20,,95,8.7
L005,C04,MUM,CAR,2023-08-05,450000,10,
L005,C04,MUM,CAR,2023-08-05,450000,10,
```

### Q1. What are Series and DataFrame?
**Answer:** A **Series** is a 1-D labelled array (one column). A **DataFrame** is a 2-D labelled table (many Series sharing an index).
- **Example 1:** `df["outstanding"]` is a Series. `df` is a DataFrame.
- **Example 2:** `pd.Series([0.02, 0.05], index=["HOME","CAR"])` is a PD per product.

### Q2. How do you load and inspect data?
```python
import pandas as pd
df = pd.read_csv("loans.csv", parse_dates=["sanction_date"])
df.head(); df.shape; df.info(); df.describe(); df.dtypes
df.isna().sum(); df["branch"].value_counts()
```
- **Example 1:** `df.info()` shows `outstanding` has 5 non-null values out of 6, so one is missing.
- **Example 2:** `value_counts()` shows MUM has 3 loans.

### Q3. `loc` vs `iloc`?
**Answer:** `loc` selects by **labels** (the end is inclusive). `iloc` selects by **integer position** (the end is exclusive).
- **Example 1:** `df.loc[df["dpd"] > 90, ["loan_id", "outstanding"]]` filters NPA loans and picks two columns.
- **Example 2:** `df.iloc[0:3, 0:2]` returns the first 3 rows and first 2 columns.

### Q4. How do you filter rows with multiple conditions?
```python
df[(df["branch"] == "MUM") & (df["dpd"] > 30)]
df[df["product"].isin(["HOME", "CAR"])]
df.query("dpd > 90 and outstanding > 100000")
```
**Gotcha:** use `&` and `|` with parentheses, not `and` / `or`.
- **Example 2:** `df[~df["loan_id"].str.startswith("L")]` finds invalid IDs.

### Q5. How do you handle missing values?
**Answer:** First **understand why** values are missing. Then drop, fill (constant, mean, median, mode, forward-fill) or flag them. In regulatory data, **don't silently fill** critical fields. Flag them and send them back to the source.
```python
df["outstanding"].isna().sum()
df["interest_rate"] = df["interest_rate"].fillna(df.groupby("product")["interest_rate"].transform("median"))
df["outstanding_missing"] = df["outstanding"].isna()     # flag for data-quality report
df = df.dropna(subset=["loan_id"])                        # key field must exist
```
- **Example 1:** A missing interest rate is filled with the product median, for analytics only.
- **Example 2:** A missing outstanding balance goes into an exception report. Never fill it with 0 for a regulatory return.

### Q6. How do you find and remove duplicates?
```python
df.duplicated().sum()                         # fully identical rows
df[df.duplicated("loan_id", keep=False)]      # all rows sharing a loan_id
df = df.drop_duplicates()                     # or subset=["loan_id"], keep="last"
```
- **Example 1:** L005 appears twice because the extract ran twice. Drop the exact duplicate.
- **Example 2:** Same loan_id with **different** balances is a real conflict. Report it; don't drop it blindly.

### Q7. groupby – how and why?
**Answer:** Split → apply → combine. It aggregates by category.
```python
df.groupby("branch")["outstanding"].sum()
df.groupby(["branch", "product"]).agg(
    loans=("loan_id", "count"),
    total_os=("outstanding", "sum"),
    avg_rate=("interest_rate", "mean"),
    max_dpd=("dpd", "max"),
).reset_index()
```
- **Example 1:** Branch-wise outstanding for an MIS report.
- **Example 2:** Gross NPA % by branch:
```python
df["is_npa"] = df["dpd"] > 90
g = df.groupby("branch").apply(lambda x: x.loc[x.is_npa, "outstanding"].sum() / x["outstanding"].sum())
```

### Q8. `apply` vs `map` vs vectorised operations?
**Answer:** Vectorised ops (`df.a * 2`, `np.where`) are the fastest. `Series.map` maps values with a dict or function. `apply` runs a Python function per row or element and is the slowest.
```python
df["bucket"] = np.select(
    [df.dpd == 0, df.dpd <= 30, df.dpd <= 60, df.dpd <= 90],
    ["Standard", "SMA-0", "SMA-1", "SMA-2"], default="NPA")
df["product_name"] = df["product"].map({"HOME": "Home Loan", "CAR": "Auto Loan"})
```
- **Example 2:** Use `apply` only for complex logic, e.g. calling an LLM per row (and batch those calls).

### Q9. merge vs join vs concat?
**Answer:** `merge` works like a SQL join on columns. `join` merges on the index. `concat` stacks DataFrames vertically or horizontally.
```python
customers = pd.DataFrame({"customer_id": ["C01","C02","C05"], "name": ["Asha","Ravi","Zoya"]})
df.merge(customers, on="customer_id", how="left")   # inner, left, right, outer
pd.concat([jan_df, feb_df], ignore_index=True)
```
- **Example 1:** Attach customer names to loans (left join keeps every loan).
- **Example 2:** Use `indicator=True` with an outer merge to find accounts in the GL but not in the extract:
```python
m = gl.merge(extract, on="account_id", how="outer", indicator=True)
m[m["_merge"] != "both"]
```

### Q10. pivot_table vs groupby?
```python
pd.pivot_table(df, index="branch", columns="product", values="outstanding",
               aggfunc="sum", fill_value=0, margins=True)
```
- **Example 1:** An Excel-style branch × product matrix, as regulators often want.
- **Example 2:** `pd.crosstab(df.branch, df.bucket)` counts loans by SMA bucket per branch.

### Q11. How do you work with dates?
```python
df["sanction_date"] = pd.to_datetime(df["sanction_date"], errors="coerce")
df["year"] = df["sanction_date"].dt.year
df["age_days"] = (pd.Timestamp("2026-11-30") - df["sanction_date"]).dt.days
monthly = df.set_index("sanction_date").resample("ME")["outstanding"].sum()
```
- **Example 1:** `errors="coerce"` turns a bad date like "31-02-2024" into NaT, which you then report.
- **Example 2:** Loan vintage analysis by sanction year.

### Q12. How do you clean string columns?
```python
df.columns = df.columns.str.strip().str.lower().str.replace(r"[^a-z0-9]+", "_", regex=True)
df["branch"] = df["branch"].str.strip().str.upper()
df["pan"].str.match(r"^[A-Z]{5}[0-9]{4}[A-Z]$")      # PAN format validation
```
- **Example 2:** "Bengaluru ", "BANGALORE" and "blr" are standardised to "BLR" with a mapping dict.

### Q13. How do you change dtypes and reduce memory?
```python
df["outstanding"] = pd.to_numeric(df["outstanding"], errors="coerce")
df["branch"] = df["branch"].astype("category")
df.memory_usage(deep=True).sum()
```
- **Example:** A branch column with 10 unique values across 5M rows uses far less memory as a category.

### Q14. How do you process a file too big for memory?
**Answer:** Read it in chunks, pick only the needed columns, and use proper dtypes. For larger data use Polars, DuckDB or Spark.
```python
total = 0
for chunk in pd.read_csv("txns.csv", usecols=["amount"], chunksize=500_000):
    total += chunk["amount"].sum()
```
- **Example 2:** DuckDB runs SQL directly on a 20 GB CSV or Parquet file: `duckdb.sql("select branch, sum(amt) from 'txns.parquet' group by 1")`.

### Q15. SettingWithCopyWarning – what and how to fix?
**Answer:** It warns that you may be modifying a temporary copy of a slice. Use `.loc` for assignment, or `.copy()` the slice. (pandas 3.0 switched to Copy-on-Write by default, which removes the ambiguity. Still use `.loc`.)
- **Example:** Write `df.loc[df.dpd > 90, "flag"] = "NPA"`, not `df[df.dpd > 90]["flag"] = "NPA"`.

### Q16. How do you write outputs?
```python
df.to_csv("out.csv", index=False)
with pd.ExcelWriter("report.xlsx") as w:
    summary.to_excel(w, sheet_name="Summary", index=False)
    exceptions.to_excel(w, sheet_name="Exceptions", index=False)
df.to_parquet("out.parquet")      # columnar, compressed, typed
df.to_sql("loans", conn, if_exists="replace", index=False)
```
- **Example:** A daily recon workbook with Summary + Exceptions sheets emailed to the ops team.

### Q17. Window / rolling / cumulative functions?
```python
df.sort_values("date").groupby("account_id")["amount"].cumsum()
s.rolling(7).mean()                  # 7-day moving average
df.groupby("branch")["outstanding"].rank(ascending=False)
df["prev_dpd"] = df.groupby("loan_id")["dpd"].shift(1)   # month-over-month change
```
- **Example 1:** Running balance per account.
- **Example 2:** Flag loans whose DPD jumped from 0 to 60 in one month (an early warning signal).

### Q18. How would you prepare a text column for a GenAI pipeline?
**Answer:** Deduplicate, strip HTML and whitespace, normalise unicode, drop empty or very short rows, mask PII, chunk long text, and keep metadata (source, date, ID) for citations.
```python
df["text"] = (df["text"].fillna("").str.replace(r"<[^>]+>", " ", regex=True)
              .str.replace(r"\s+", " ", regex=True).str.strip())
df = df[df["text"].str.len() > 30].drop_duplicates("text")
df["text"] = df["text"].str.replace(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", "<PAN>", regex=True)
```
- **Example 1:** Customer complaint texts cleaned before classification by an LLM.
- **Example 2:** Circular paragraphs with `circular_no` and `date` kept as metadata for RAG citations.
