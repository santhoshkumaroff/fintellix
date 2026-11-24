# Python Data Structures (JD: "Strong fundamentals – data structures")

### Q1. What are Python's built-in data structures?
**Answer:** **list** (ordered, mutable), **tuple** (ordered, immutable), **set** (unordered, unique, mutable), **dict** (key→value, insertion-ordered since 3.7, mutable). Plus **str** (immutable sequence of characters) and **frozenset** (immutable set).
- **Example 1:** `branches = ["BLR", "MUM"]` (list), `coords = (12.97, 77.59)` (tuple).
- **Example 2:** `unique_customers = {"C1", "C2"}` (set), `balance = {"C1": 5000}` (dict).

### Q2. List vs tuple?
**Answer:** A list is mutable (you can append or change it). A tuple is immutable, slightly faster, uses less memory, and is **hashable if all its elements are hashable**, so it can be a dict key or a set element. Use a tuple for fixed records and a list for collections that grow.
- **Example 1:** `report_period = ("2026-Q3", "RBI")` should not change, so use a tuple.
- **Example 2:** `failed_validations = []` grows as checks fail, so use a list.
```python
rates = {("HOME", "FIXED"): 8.5}   # tuple as dict key works
# {["HOME","FIXED"]: 8.5}          # TypeError: unhashable type: 'list'
```

### Q3. List vs set? When would you use a set?
**Answer:** Use a set for uniqueness and fast membership tests. `x in set` is O(1) on average, while `x in list` is O(n). Sets also support union (`|`), intersection (`&`) and difference (`-`).
- **Example 1:** Find accounts in the GL but missing in the loan extract: `gl_accounts - extract_accounts`.
- **Example 2:** Deduplicate customer IDs: `len(set(customer_ids))`.

### Q4. How does a dictionary work internally?
**Answer:** A hash table. Python hashes the key to find a slot, so lookup, insert and delete are O(1) on average. Keys must be **hashable** (immutable types such as str, int, tuple). Since Python 3.7, dicts preserve insertion order.
- **Example 1:** `rate_by_product = {"HOME": 8.5, "CAR": 9.2}`; `rate_by_product["CAR"]` is an instant lookup.
- **Example 2:** Counting transactions per customer:
```python
counts = {}
for c in ["C1", "C2", "C1"]:
    counts[c] = counts.get(c, 0) + 1   # {'C1': 2, 'C2': 1}
```

### Q5. Mutable vs immutable – why does it matter?
**Answer:** Mutable objects (list, dict, set) can change in place. Immutable ones (int, float, str, tuple, frozenset) cannot, so "changing" them creates a new object. This matters for function arguments, dict keys and default arguments.
- **Example 1:** `s = "abc"; s.upper()` returns a new string, and `s` is still `"abc"`.
- **Example 2:** Passing a list to a function that appends to it changes the caller's list too.

### Q6. Shallow copy vs deep copy?
**Answer:** A shallow copy (`list.copy()`, `copy.copy`, `lst[:]`) creates a new outer container but shares the inner objects. A deep copy (`copy.deepcopy`) copies everything recursively.
```python
import copy
a = [[1, 2], [3, 4]]
b = a.copy();  b[0].append(99)   # a is [[1, 2, 99], [3, 4]] – inner list shared!
c = copy.deepcopy(a); c[0].append(7)  # a unchanged
```
- **Example 1:** Copying a nested report config before modifying it for a test needs `deepcopy`.
- **Example 2:** A pandas `df.copy()` is deep by default for data. Without it, slicing can trigger SettingWithCopy issues in older pandas.

### Q7. `==` vs `is`?
**Answer:** `==` compares **values**. `is` compares **identity** (the same object in memory). Use `is` only for `None`, `True` and `False`.
- **Example 1:** `[1,2] == [1,2]` → True; `[1,2] is [1,2]` → False.
- **Example 2:** `if value is None:` is the correct way to check for missing values.

### Q8. What is list comprehension? Dict/set comprehension?
**Answer:** A concise way to build a collection from an iterable, with an optional filter. It is usually faster and more readable than a loop with append.
- **Example 1:** NPA accounts: `npa = [a["id"] for a in loans if a["dpd"] > 90]`.
- **Example 2:** Map of id → balance: `{a["id"]: a["bal"] for a in loans}`. Unique branches: `{a["branch"] for a in loans}`.

### Q9. What is a generator? Generator vs list?
**Answer:** A generator produces values lazily, one at a time, using `yield` or `(x for x in ...)`. It doesn't store everything in memory. Use it for large files or streams. A list holds all items in memory at once.
- **Example 1:** Reading a 10 GB transaction file line by line:
```python
def read_rows(path):
    with open(path) as f:
        for line in f:
            yield line.rstrip("\n").split(",")
```
- **Example 2:** `total = sum(t["amount"] for t in transactions)` computes the total without building a list.

### Q10. What is slicing?
**Answer:** `seq[start:stop:step]`. `stop` is excluded. Negative indices count from the end.
- **Example 1:** `"ACC000123"[3:]` → `"000123"`; `last3 = txns[-3:]`.
- **Example 2:** `s[::-1]` reverses a string (palindrome check).

### Q11. How do you sort a list of dicts by a field?
**Answer:** `sorted(iterable, key=..., reverse=...)` returns a new list. `list.sort()` sorts in place and returns None. Both are stable (Timsort, O(n log n)).
- **Example 1:** Top borrowers: `sorted(loans, key=lambda x: x["bal"], reverse=True)[:10]`.
- **Example 2:** Sort by branch, then by balance descending: `sorted(loans, key=lambda x: (x["branch"], -x["bal"]))`.

### Q12. What are `collections.Counter`, `defaultdict`, `deque`, `namedtuple`?
- **Counter:** counts items. `Counter(["BLR","MUM","BLR"]).most_common(1)` → `[('BLR', 2)]`.
- **defaultdict:** auto-creates missing keys. Example: group accounts by branch:
```python
from collections import defaultdict
by_branch = defaultdict(list)
for a in loans: by_branch[a["branch"]].append(a["id"])
```
- **deque:** fast appends and pops at both ends. Example: keep the last 5 chat messages for an LLM's memory: `deque(maxlen=5)`.
- **namedtuple:** a readable immutable record: `Loan = namedtuple("Loan", "id bal dpd")`.

### Q13. Time complexity of common operations?
| Operation | list | dict/set |
|---|---|---|
| index / lookup | O(1) by index | O(1) avg by key |
| `x in` | O(n) | O(1) avg |
| append | O(1) amortised | — |
| insert at start / pop(0) | O(n) | — |
| sort | O(n log n) | — |
- **Example:** Checking 1 lakh transaction IDs against a blacklist of 10,000: a set takes milliseconds, a list takes much longer.

### Q14. How do you merge two dicts?
**Answer:** `merged = {**d1, **d2}` or (Python 3.9+) `d1 | d2`. On key conflicts the right-hand dict wins.
- **Example 1:** Default config + client config: `cfg = default_cfg | client_cfg`.
- **Example 2:** In place: `d1.update(d2)`.

### Q15. How do you remove duplicates from a list but keep order?
**Answer:** `list(dict.fromkeys(items))`. Dicts keep insertion order, and `set()` would lose it.
- **Example:** `list(dict.fromkeys(["C2","C1","C2"]))` → `["C2","C1"]`.

### Q16. What is a string and common string methods?
**Answer:** Immutable Unicode text. Key methods: `strip`, `split`, `join`, `replace`, `lower/upper`, `startswith`, `find`, f-strings.
- **Example 1:** Clean a messy column header: `" Cust Name ".strip().lower().replace(" ", "_")` → `"cust_name"`.
- **Example 2:** Build a log message: `f"{acc_id}: DPD={dpd}, NPA={dpd>90}"`.

### Q17. What is `*args` unpacking for sequences? `zip`, `enumerate`?
- `zip(a, b)` pairs items: `dict(zip(ids, balances))`.
- `enumerate(seq, start=1)` gives index + value: `for i, row in enumerate(rows, 1): print(i, row)`, useful for reporting the line number of a bad row.
- Unpacking: `first, *rest = [1,2,3]` → `first=1, rest=[2,3]`.
