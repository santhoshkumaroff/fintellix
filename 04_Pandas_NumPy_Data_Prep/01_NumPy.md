# NumPy (JD: "Pandas, NumPy")

### Q1. What is NumPy and why is it faster than Python lists?
**Answer:** NumPy provides the `ndarray`: a fixed-type, contiguous block of memory with vectorised operations implemented in C. There's no per-element Python loop and no per-element type checks, so it's typically 10–100× faster.
- **Example 1:** Apply a 2% interest to 1 million balances: `balances * 1.02` (vectorised) vs a Python loop.
- **Example 2:** Embedding vectors (e.g. 384 or 1024 floats) are stored as NumPy arrays for similarity search.

### Q2. List vs NumPy array?
| list | ndarray |
|---|---|
| Mixed types | One dtype |
| `+` concatenates | `+` adds element-wise |
| Slow loops | Vectorised C ops |
- **Example:** `[1,2] + [3,4]` → `[1,2,3,4]`; `np.array([1,2]) + np.array([3,4])` → `[4, 6]`.

### Q3. Creating arrays?
```python
import numpy as np
np.array([1, 2, 3]); np.zeros((3, 4)); np.ones(5); np.arange(0, 10, 2)
np.linspace(0, 1, 5); np.random.default_rng(42).normal(size=100)
```
- **Example 2:** `np.zeros(len(df))` as a starting array for provision amounts.

### Q4. What are shape, ndim, dtype, reshape?
```python
a = np.arange(12)          # shape (12,)
b = a.reshape(3, 4)        # shape (3, 4), ndim 2
b.dtype                    # int64
```
- **Example 1:** 12 monthly NPA values reshaped to (4 quarters, 3 months) to sum by quarter: `b.sum(axis=1)`.
- **Example 2:** A batch of 32 embeddings of size 384 has shape `(32, 384)`.

### Q5. What is broadcasting?
**Answer:** NumPy stretches smaller arrays to match shapes for element-wise operations, without copying data. Rule: dimensions are compared from the right, and each pair must be equal or 1.
- **Example 1:** `balances (1000, 3 months) * rates (3,)` multiplies each month's column by its rate.
- **Example 2:** Normalising embeddings: `X / np.linalg.norm(X, axis=1, keepdims=True)`, where shape (n, d) is divided by (n, 1).

### Q6. Boolean indexing / masking?
```python
dpd = np.array([0, 45, 95, 200, 10])
dpd[dpd > 90]              # array([ 95, 200])
np.where(dpd > 90, "NPA", "STD")
```
- **Example 2:** Cap outliers: `amounts[amounts > 1e8] = 1e8`.

### Q7. axis=0 vs axis=1?
**Answer:** `axis=0` operates **down the rows** (one result per column). `axis=1` operates **across the columns** (one result per row).
- **Example:** `monthly.sum(axis=0)` gives a total per month (column). `monthly.sum(axis=1)` gives a total per account (row).

### Q8. How do you compute cosine similarity with NumPy? (GenAI link – likely asked)
```python
def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

q = np.array([0.1, 0.9, 0.2])
docs = np.array([[0.1, 0.8, 0.3], [0.9, 0.1, 0.0]])
docs_n = docs / np.linalg.norm(docs, axis=1, keepdims=True)
q_n = q / np.linalg.norm(q)
scores = docs_n @ q_n          # one score per doc
top = np.argsort(scores)[::-1] # best first
```
- **Example 1:** A question about "NPA classification" scores highest against the NPA circular chunk.
- **Example 2:** Finding near-duplicate customer names by comparing their embeddings.

### Q9. View vs copy?
**Answer:** Slicing returns a **view** (shared memory), so modifying it changes the original. `.copy()` makes an independent array. Fancy and boolean indexing return copies.
- **Example:** `sub = a[:5]; sub[0] = 99` → `a[0]` is now 99.

### Q10. Useful functions?
`np.sum, mean, median, std, percentile, argmax, argsort, unique(return_counts=True), cumsum, clip, isnan, nan_to_num, concatenate, vstack, hstack`.
- **Example 1:** `np.percentile(loan_amounts, 99)` gives the threshold for outlier review.
- **Example 2:** `np.unique(branches, return_counts=True)` counts loans per branch.

### Q11. How do you handle NaN in NumPy?
**Answer:** `np.nan` propagates (`np.sum([1, np.nan])` → nan). Use `np.nansum`, `np.nanmean` and `np.isnan` masks.
- **Example:** `np.nanmean(interest_rates)` ignores missing rates.
