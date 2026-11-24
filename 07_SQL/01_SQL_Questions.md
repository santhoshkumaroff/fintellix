# SQL (JD Good-to-have: "Joins, aggregations, subqueries")

### Practice schema (create it in SQLite: `sqlite3 bank.db`)
```sql
CREATE TABLE customers (customer_id TEXT PRIMARY KEY, name TEXT, city TEXT, segment TEXT);
CREATE TABLE loans (loan_id TEXT PRIMARY KEY, customer_id TEXT, branch TEXT, product TEXT,
                    outstanding REAL, dpd INTEGER, sanction_date DATE);
CREATE TABLE payments (payment_id INTEGER PRIMARY KEY, loan_id TEXT, pay_date DATE, amount REAL);

INSERT INTO customers VALUES ('C01','Asha','Bengaluru','Retail'),('C02','Ravi','Mumbai','Retail'),
 ('C03','Zen Corp','Delhi','Corporate'),('C04','Meera','Mumbai','Retail'),('C05','Arun','Chennai','Retail');
INSERT INTO loans VALUES ('L001','C01','BLR','HOME',2500000,0,'2022-04-01'),('L002','C02','MUM','CAR',600000,45,'2023-01-15'),
 ('L003','C01','BLR','PERSONAL',200000,120,'2024-06-10'),('L004','C03','DEL','TERM',50000000,95,'2021-11-20'),
 ('L005','C04','MUM','CAR',450000,10,'2023-08-05');
INSERT INTO payments (loan_id,pay_date,amount) VALUES ('L001','2026-10-05',25000),('L002','2026-08-15',15000),('L005','2026-10-07',12000);
```

### Q1. What are the types of SQL commands?
**Answer:** **DDL** (CREATE, ALTER, DROP, TRUNCATE), **DML** (INSERT, UPDATE, DELETE), **DQL** (SELECT), **DCL** (GRANT, REVOKE), **TCL** (COMMIT, ROLLBACK, SAVEPOINT).
- **Example 1:** `GRANT SELECT ON loans TO finbot_user;` gives a text-to-SQL bot read-only access.
- **Example 2:** Wrap a batch of provision updates in a transaction and `ROLLBACK` if validation fails.

### Q2. Explain the JOIN types.
**Answer:** **INNER** = only matching rows. **LEFT** = all left rows plus matches (NULL if none). **RIGHT** = the reverse. **FULL OUTER** = all rows from both. **CROSS** = every combination. **SELF** = a table joined with itself.
```sql
-- Loans with customer names
SELECT l.loan_id, c.name, l.outstanding
FROM loans l INNER JOIN customers c ON l.customer_id = c.customer_id;

-- Customers with NO loans (anti-join)
SELECT c.* FROM customers c LEFT JOIN loans l ON c.customer_id = l.customer_id
WHERE l.loan_id IS NULL;          -- returns C05 Arun
```
- **Example 2:** Loans with no payment this month: `loans LEFT JOIN payments ... WHERE p.payment_id IS NULL`.

### Q3. WHERE vs HAVING?
**Answer:** `WHERE` filters rows **before** grouping. `HAVING` filters groups **after** aggregation.
```sql
SELECT branch, SUM(outstanding) AS total
FROM loans
WHERE product <> 'TERM'          -- row filter
GROUP BY branch
HAVING SUM(outstanding) > 500000; -- group filter
```
- **Example 2:** Customers with more than 1 loan: `GROUP BY customer_id HAVING COUNT(*) > 1` → C01.

### Q4. Order of execution of a SELECT?
**Answer:** `FROM/JOIN → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT`.
- **Example:** That's why you can't use a SELECT alias in WHERE in most databases, but you can in ORDER BY.

### Q5. Aggregations – total, count, average NPA by branch
```sql
SELECT branch,
       COUNT(*)                                            AS loans,
       SUM(outstanding)                                    AS total_os,
       SUM(CASE WHEN dpd > 90 THEN outstanding ELSE 0 END) AS npa_os,
       ROUND(100.0 * SUM(CASE WHEN dpd > 90 THEN outstanding ELSE 0 END) / SUM(outstanding), 2) AS gnpa_pct
FROM loans GROUP BY branch ORDER BY gnpa_pct DESC;
```
- **Example 2:** `COUNT(*)` counts all rows. `COUNT(col)` skips NULLs. `COUNT(DISTINCT customer_id)` counts unique borrowers.

### Q6. What is a subquery? Correlated vs non-correlated?
**Answer:** A query inside another query. A **non-correlated** subquery runs once. A **correlated** subquery references the outer row and conceptually runs per row.
```sql
-- Non-correlated: loans above average outstanding
SELECT * FROM loans WHERE outstanding > (SELECT AVG(outstanding) FROM loans);

-- Correlated: loans that are the largest in their branch
SELECT * FROM loans l1
WHERE outstanding = (SELECT MAX(outstanding) FROM loans l2 WHERE l2.branch = l1.branch);
```
- **Example 2:** `WHERE customer_id IN (SELECT customer_id FROM customers WHERE segment = 'Corporate')`.

### Q7. IN vs EXISTS?
**Answer:** `EXISTS` stops at the first match and handles NULLs safely. `NOT IN` with a NULL in the subquery returns no rows (a classic trap). Prefer `NOT EXISTS`.
```sql
SELECT * FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM loans l WHERE l.customer_id = c.customer_id);
```

### Q8. What is a CTE (WITH clause)?
**Answer:** A named temporary result used to make complex queries readable. It can be recursive.
```sql
WITH cust_exposure AS (
  SELECT customer_id, SUM(outstanding) AS exposure FROM loans GROUP BY customer_id
)
SELECT c.name, e.exposure FROM cust_exposure e JOIN customers c USING (customer_id)
ORDER BY e.exposure DESC LIMIT 3;
```
- **Example 2:** A recursive CTE walks a parent→child company hierarchy to compute group exposure.

### Q9. Window functions – ROW_NUMBER, RANK, DENSE_RANK, LAG, running total
```sql
-- Rank loans by outstanding within each branch
SELECT loan_id, branch, outstanding,
       ROW_NUMBER() OVER (PARTITION BY branch ORDER BY outstanding DESC) AS rn,
       RANK()       OVER (ORDER BY outstanding DESC) AS rnk,
       SUM(outstanding) OVER (PARTITION BY branch) AS branch_total
FROM loans;

-- Month-over-month change in payments
SELECT loan_id, pay_date, amount,
       amount - LAG(amount) OVER (PARTITION BY loan_id ORDER BY pay_date) AS change
FROM payments;
```
**RANK vs DENSE_RANK:** with values 100, 100, 90, RANK gives 1, 1, 3 and DENSE_RANK gives 1, 1, 2.
- **Example:** Top 2 loans per branch: wrap the query and filter `WHERE rn <= 2`.

### Q10. Find the 2nd highest outstanding (classic)
```sql
SELECT MAX(outstanding) FROM loans WHERE outstanding < (SELECT MAX(outstanding) FROM loans);
-- or
SELECT outstanding FROM (SELECT outstanding, DENSE_RANK() OVER (ORDER BY outstanding DESC) r FROM loans) t WHERE r = 2;
```

### Q11. Find duplicates
```sql
SELECT loan_id, COUNT(*) FROM loans GROUP BY loan_id HAVING COUNT(*) > 1;
```
- **Example 2:** Delete duplicates while keeping one: use `ROW_NUMBER() OVER (PARTITION BY loan_id ORDER BY ...)` and delete the rows where rn > 1.

### Q12. CASE WHEN – bucket loans by DPD
```sql
SELECT loan_id, dpd,
  CASE WHEN dpd = 0 THEN 'Standard'
       WHEN dpd <= 30 THEN 'SMA-0'
       WHEN dpd <= 60 THEN 'SMA-1'
       WHEN dpd <= 90 THEN 'SMA-2'
       ELSE 'NPA' END AS bucket
FROM loans;
```

### Q13. DELETE vs TRUNCATE vs DROP?
**Answer:** DELETE removes chosen rows, can have WHERE, is logged, and can be rolled back. TRUNCATE removes all rows quickly, has no WHERE, and resets storage. DROP removes the table itself.
- **Example:** Reloading a staging table every night → TRUNCATE then INSERT.

### Q14. UNION vs UNION ALL?
**Answer:** UNION removes duplicates (slower, because it sorts or hashes). UNION ALL keeps everything (faster).
- **Example:** Combining Jan and Feb transaction tables → UNION ALL (duplicates aren't expected, and you don't want to lose genuine repeats).

### Q15. Primary key, foreign key, unique, index?
**Answer:** A **primary key** uniquely identifies a row (not null). A **foreign key** references another table's key (referential integrity). **UNIQUE** prevents duplicates. An **index** speeds up lookups and joins but slows writes.
- **Example 1:** `loans.customer_id` is a foreign key to `customers.customer_id`, so it rejects loans for non-existent customers.
- **Example 2:** An index on `loans(branch, snapshot_month)` speeds up monthly branch reports.

### Q16. What is normalisation? 1NF, 2NF, 3NF?
**Answer:** Organising tables to reduce redundancy. **1NF:** atomic values, no repeating groups. **2NF:** 1NF plus no partial dependency on part of a composite key. **3NF:** 2NF plus no transitive dependency (non-key → non-key).
- **Example 1:** Storing "phone1, phone2, phone3" columns violates 1NF. Use a separate phones table.
- **Example 2:** Storing branch_city inside the loans table (it depends on branch, not the loan) violates 3NF. Move it to a branches table.
- Note: data warehouses deliberately **denormalise** (star schema) for fast reads. See `08_Data_Warehousing_ETL`.

### Q17. What are ACID properties?
**Answer:** **Atomicity** (all or nothing), **Consistency** (valid state to valid state), **Isolation** (concurrent transactions don't interfere), **Durability** (committed data survives crashes).
- **Example:** A fund transfer debits A and credits B. Atomicity guarantees you never get only the debit.

### Q18. How do you run SQL from Python?
```python
import sqlite3, pandas as pd
conn = sqlite3.connect("bank.db")
df = pd.read_sql("SELECT branch, SUM(outstanding) total FROM loans GROUP BY branch", conn)
# Parameterised – prevents SQL injection
pd.read_sql("SELECT * FROM loans WHERE branch = ?", conn, params=("MUM",))
conn.close()
```
- **Example 2:** Production databases use SQLAlchemy engines (`create_engine("postgresql://...")`).

### Q19. What is SQL injection and how do you prevent it?
**Answer:** Malicious input changes your query (`' OR 1=1 --`). Prevent it with **parameterised queries**, least-privilege DB users and input validation. For LLM text-to-SQL: read-only user, SELECT-only check, table allow-list.

### Q20. Write: customers whose total exposure exceeds ₹10 lakh and who have at least one NPA loan
```sql
SELECT c.name, SUM(l.outstanding) AS exposure
FROM customers c JOIN loans l ON c.customer_id = l.customer_id
GROUP BY c.customer_id, c.name
HAVING SUM(l.outstanding) > 1000000
   AND SUM(CASE WHEN l.dpd > 90 THEN 1 ELSE 0 END) >= 1;
-- Result: Asha (2.7M, has L003 NPA), Zen Corp (50M, L004 NPA)
```
