# Data Warehousing & ETL (JD Good-to-have: "ETL/ELT, fact and dimension tables, star/snowflake schemas")

> This is how Fintellix's platform works under the hood: many bank source systems → integration → a standard data model → reports.

### Q1. What is a data warehouse?
**Answer:** A central repository of integrated, cleaned, historical data from many source systems, optimised for **analysis and reporting** (OLAP), not day-to-day transactions (OLTP).
- **Example 1:** A bank's warehouse combines core banking, cards, treasury and the GL so the regulatory team can report from one place.
- **Example 2:** RBI's CIMS is itself described as a "next generation data warehouse" for supervisory data.

### Q2. OLTP vs OLAP?
| OLTP | OLAP |
|---|---|
| Day-to-day transactions (insert/update) | Analysis, aggregation |
| Normalised | Denormalised (star) |
| Current data | Historical data |
| e.g. Core banking system | e.g. Regulatory reporting warehouse |
- **Example:** An ATM withdrawal updates the OLTP core banking system. Monthly NPA trend analysis runs on OLAP.

### Q3. What is ETL? What is ELT? Difference?
**Answer:** **ETL** = Extract → Transform (on a separate engine) → Load into the warehouse. **ELT** = Extract → Load raw data into the warehouse or lake → Transform inside it using its compute (e.g. SQL / dbt). ELT suits modern cloud warehouses (Snowflake, BigQuery, Databricks).
- **Example 1, ETL:** An Informatica job cleans loan data, then loads it into an Oracle DW.
- **Example 2, ELT:** Load the raw CSVs into BigQuery, then transform them with SQL/dbt into reporting tables.

### Q4. What happens in each ETL step?
- **Extract:** full or incremental pulls from sources (DB, files, APIs).
- **Transform:** cleanse, standardise, deduplicate, map codes, derive fields (DPD buckets), aggregate, apply business rules, validate.
- **Load:** insert or upsert into target tables. Full refresh vs incremental. Maintain history.
- **Example:** Source `prod_cd = 'HL'` is mapped to the standard `product = 'HOME_LOAN'` during transform.

### Q5. What are fact and dimension tables?
**Answer:** A **fact table** stores measurable events or numbers (amounts, counts) plus foreign keys. **Dimension tables** store descriptive context (who, what, where, when) used to filter and group.
- **Example 1:** `fact_loan_snapshot(date_key, loan_key, branch_key, product_key, outstanding, dpd, provision)`.
- **Example 2:** `dim_branch(branch_key, branch_code, city, state, region)`, `dim_date(date_key, date, month, quarter, fiscal_year)`.

### Q6. What is a star schema vs a snowflake schema?
**Answer:** **Star:** a central fact table with denormalised dimensions directly attached. Simple, few joins, fast. **Snowflake:** dimensions are normalised into sub-dimensions (branch → city → state). Less redundancy, more joins.
```
STAR:                          SNOWFLAKE:
 dim_date   dim_product         dim_product -> dim_product_category
      \      /                        |
   fact_loan_snapshot           fact_loan_snapshot
      /      \                        |
 dim_branch  dim_customer        dim_branch -> dim_city -> dim_state
```
- **Example 1:** BI dashboards prefer star for speed.
- **Example 2:** Snowflake suits a huge geography hierarchy maintained separately.

### Q7. What is grain?
**Answer:** The level of detail that one fact row represents. Define it first.
- **Example 1:** "One row per loan per month-end" (a monthly snapshot fact).
- **Example 2:** "One row per payment transaction" (a transaction fact).

### Q8. Types of fact tables?
- **Transaction fact:** one row per event (each payment).
- **Periodic snapshot:** the state at regular intervals (month-end loan balances). Very common in regulatory reporting.
- **Accumulating snapshot:** one row per process instance, updated through milestones (loan application → sanctioned → disbursed).

### Q9. What are Slowly Changing Dimensions (SCD)? Type 1 vs Type 2?
**Answer:** How you handle dimension attributes that change over time.
- **Type 1:** overwrite (no history). *Example:* fix a typo in a customer's name.
- **Type 2:** add a new row with `valid_from`, `valid_to` and `is_current` (full history). *Example:* a customer moves from Bengaluru to Mumbai. Reports for last year must still show Bengaluru.
- **Type 3:** keep the previous value in an extra column (limited history).
| customer_key | customer_id | city | valid_from | valid_to | is_current |
|---|---|---|---|---|---|
| 101 | C01 | Bengaluru | 2020-01-01 | 2026-06-30 | N |
| 245 | C01 | Mumbai | 2026-07-01 | 9999-12-31 | Y |
- Regulators may ask for **as-of** data, which is why Type 2 matters in banking.

### Q10. Surrogate key vs natural key?
**Answer:** A natural key comes from the business (loan_id, PAN). A surrogate key is a system-generated integer used in the warehouse. Surrogate keys enable SCD2 (multiple versions of the same customer), are stable when source IDs change, and make joins faster.
- **Example:** Two source systems both use `customer_id = 1001` for different people. Surrogate keys keep them distinct.

### Q11. Data lake vs data warehouse vs lakehouse?
**Answer:** A **lake** stores raw data of any format cheaply (S3, ADLS), with schema-on-read. A **warehouse** holds structured, modelled data with schema-on-write. A **lakehouse** (Databricks Delta, Iceberg) adds warehouse features (ACID, schemas) on top of the lake.
- **Example:** Fintellix lists "data lake and analytics" for the Philippines. Raw bank extracts land in the lake, and curated reporting tables are built on top.

### Q12. What is a data mart?
**Answer:** A subject-specific subset of the warehouse.
- **Example 1:** A credit-risk mart (loans, collateral, provisions).
- **Example 2:** A liquidity mart (cash flows, HQLA) for LCR reporting.

### Q13. Full load vs incremental load? What is CDC?
**Answer:** A full load reloads everything (simple, heavy). An incremental load takes only new or changed rows, using a timestamp, an ID or **CDC (Change Data Capture)**, which reads changes from database logs.
- **Example 1:** A 10-row branch master → full load.
- **Example 2:** A 50M-row transactions table → incremental by `txn_date > last_loaded_date`.

### Q14. What data quality checks belong in an ETL pipeline?
**Answer:** Row counts (source vs target), null checks on keys, referential integrity, range and format checks, duplicates, reconciliation of amounts to control totals, freshness. Failed rows go to an exception table.
- **Example 1:** Source has 1,00,000 rows and the target loaded 99,950. 50 rows went to the exception table with their reasons.
- **Example 2:** Total outstanding in the fact table must equal the GL loan balance within a tolerance.

### Q15. How does this connect to regulatory reporting / Fintellix?
**Answer:** Source systems → staging (raw) → **standard data model** (like a warehouse, with conformed dimensions such as customer, product, branch, and facts such as loans, deposits, GL) → validations and rule engine → regulatory templates → submission. Lineage traces template cells back to fact rows.
- **Example 1:** One `fact_loan_snapshot` feeds the NPA return, the large exposures return and the ECL computation.
- **Example 2:** When RBI adds a "loan purpose" dimension, you add it to `dim_loan` once and every report can use it.

### Q16. Name some ETL / data tools.
Informatica, Talend, SSIS, Apache Airflow (orchestration), dbt (transformations in SQL), Apache Spark / PySpark (big data), Kafka (streaming), cloud services (AWS Glue, Azure Data Factory, GCP Dataflow).
- **Example:** Airflow schedules a daily DAG: extract (Python) → load (BigQuery) → transform (dbt) → validate (Great Expectations) → report.
