# Python Concepts & Tricky Questions (commonly asked to freshers)

### Q1. Is Python compiled or interpreted?
**Answer:** Both, in a sense. CPython compiles source to **bytecode** (`.pyc`), and the Python Virtual Machine interprets that bytecode. It's dynamically typed and strongly typed.
- **Example 1:** `"5" + 5` → TypeError (strong typing: no silent conversion).
- **Example 2:** `x = 5; x = "five"` is allowed (dynamic typing: the variable's type can change).

### Q2. What is the GIL? Threading vs multiprocessing vs asyncio?
**Answer:** The Global Interpreter Lock lets only one thread run Python bytecode at a time in CPython. So:
- **I/O-bound work** (API calls, file and network) → `threading` or `asyncio` works well, because threads wait on I/O.
- **CPU-bound work** (heavy computation) → `multiprocessing` (separate processes, each with its own GIL).
- **Example 1:** Calling the Claude API for 500 documents → asyncio or a thread pool gives a big speed-up.
```python
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=8) as ex:
    summaries = list(ex.map(summarise_doc, docs))
```
- **Example 2:** Computing ECL with heavy math for 10M rows → vectorise with NumPy, or use multiprocessing.
- (Python 3.13+ ships an optional free-threaded build without the GIL; it's fine to mention.)

### Q3. How is memory managed in Python?
**Answer:** Mostly by reference counting, plus a cyclic garbage collector for reference cycles. Objects live on a private heap.
- **Example:** `del big_df` drops a reference. When the count reaches 0, the memory is freed.

### Q4. What will this print?
```python
a = [1, 2, 3]
b = a
b.append(4)
print(a)   # [1, 2, 3, 4] – b and a are the same object
```
```python
x = 10
def f(): x = 20
f(); print(x)   # 10 – assignment inside f created a local x
```
```python
print(0.1 + 0.2 == 0.3)   # False – floating point error
```
**Money tip:** Never use float for currency in reconciliation. Use `decimal.Decimal` or integer paise.
```python
from decimal import Decimal
Decimal("0.1") + Decimal("0.2") == Decimal("0.3")   # True
```
- **Example 2:** Summing 1 million float amounts can drift by a few paise, enough to create a recon break.

### Q5. `append` vs `extend`?
- `[1,2].append([3,4])` → `[1, 2, [3, 4]]`
- `[1,2].extend([3,4])` → `[1, 2, 3, 4]`

### Q6. `range` vs list?
**Answer:** `range` is a lazy sequence object. It doesn't store every number.
- **Example:** `range(10**9)` uses tiny memory. `list(range(10**9))` would exhaust RAM.

### Q7. What are iterators and iterables?
**Answer:** An **iterable** can be looped over (it has `__iter__`). An **iterator** produces the next value with `__next__` and is exhausted after one pass.
- **Example 1:** A file object is an iterator. After looping once, a second loop yields nothing.
- **Example 2:** `it = iter([1,2]); next(it)` → 1.

### Q8. What is `pass`, `continue`, `break`?
- `pass`: do nothing (a placeholder).
- `continue`: skip to the next loop iteration. Example: skip header rows.
- `break`: exit the loop. Example: stop at the first failed critical validation.

### Q9. What is the walrus operator `:=`?
**Answer:** It assigns inside an expression (Python 3.8+).
- **Example:** `while (chunk := f.read(1024)):` processes a file in chunks.

### Q10. What's new/useful in modern Python (3.10+)?
- `match` statement (structural pattern matching)
- Better error messages, `dict | dict`, `str.removeprefix()`
- Example:
```python
match report_type:
    case "NPA": run_npa()
    case "LCR" | "NSFR": run_liquidity()
    case _: raise ValueError(report_type)
```

### Q11. How would you write a unit test?
**Answer:** Use `pytest`: write `test_*.py` files with plain `assert` statements.
```python
# test_rules.py
from rules import classify_dpd
def test_npa_boundary():
    assert classify_dpd(90) == "SMA-2"
    assert classify_dpd(91) == "NPA"
```
Run it with `pytest -q`.
- **Example 2:** Test the RAG prompt builder: given 2 chunks, the prompt must contain both chunk IDs.

### Q12. What is `enumerate`, `zip`, `any`, `all`?
- `any(row["bal"] < 0 for row in rows)` → is there at least one negative balance?
- `all(col in df.columns for col in REQUIRED)` → are all mandatory columns present?

### Q13. How do you reverse a string, check a palindrome, count characters?
```python
s = "level"
s[::-1] == s                 # palindrome
from collections import Counter
Counter("banking")           # char counts
```

### Q14. What is `__str__` vs `__repr__`?
**Answer:** `__str__` is the readable, user-facing form. `__repr__` is the unambiguous developer form, ideally valid code to recreate the object.
- **Example:** `str(Decimal("1.0"))` → `1.0`; `repr(Decimal("1.0"))` → `Decimal('1.0')`.

### Q15. What is PEP 8?
**Answer:** Python's style guide: 4-space indents, `snake_case` for functions, `PascalCase` for classes, lines around 79–99 chars, meaningful names. Tools such as `black`, `ruff` and `flake8` enforce it.
- **Example:** `def calc_npa_ratio(...)` is good. `def CalcNPA(...)` is not, for a function.
