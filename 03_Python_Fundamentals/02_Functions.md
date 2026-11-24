# Python Functions (JD: "functions")

### Q1. What is a function? Why use functions?
**Answer:** A named, reusable block of code defined with `def`. Functions avoid repetition, make code testable, and hide details behind a clear name.
- **Example 1:** `def classify_dpd(dpd): return "NPA" if dpd > 90 else "Standard"`, used for every loan.
- **Example 2:** `def clean_column_names(df): ...`, reused across every client file.

### Q2. Difference between parameters and arguments? Positional vs keyword?
**Answer:** Parameters are the names in the definition. Arguments are the values you pass. Positional arguments match by order, keyword arguments match by name.
```python
def ecl(ead, pd_, lgd): return ead * pd_ * lgd
ecl(1_000_000, 0.02, 0.4)               # positional
ecl(lgd=0.4, ead=1_000_000, pd_=0.02)   # keyword – order doesn't matter
```
- **Example 2:** `pd.read_csv("loans.csv", sep="|", dtype=str)` uses keyword arguments for clarity.

### Q3. What are `*args` and `**kwargs`?
**Answer:** `*args` collects extra positional arguments into a tuple. `**kwargs` collects extra keyword arguments into a dict.
- **Example 1:** `def total(*amounts): return sum(amounts)`; `total(100, 200, 300)`.
- **Example 2:** A wrapper that passes options through to the LLM API:
```python
def ask_llm(prompt, **kwargs):
    return client.messages.create(messages=[{"role":"user","content":prompt}], **kwargs)
ask_llm("Summarise", model="claude-sonnet-5-5", max_tokens=300)
```

### Q4. What are default arguments? What's the mutable default trap?
**Answer:** Defaults are evaluated **once**, when the function is defined. A mutable default (list or dict) is shared across calls.
```python
def add_error(msg, errors=[]):      # BUG
    errors.append(msg); return errors
add_error("a"); add_error("b")     # ['a', 'b'] – leaked!

def add_error(msg, errors=None):    # FIX
    if errors is None: errors = []
    errors.append(msg); return errors
```
- **Example 2:** A validation function that collects failed rule IDs. With the bug, failures from file 1 appear in file 2's report.

### Q5. What is a lambda function?
**Answer:** A small anonymous one-expression function, mainly used as a `key` or in `map`, `filter` and `apply`.
- **Example 1:** `sorted(loans, key=lambda x: x["dpd"], reverse=True)`.
- **Example 2:** `df["bucket"] = df["dpd"].apply(lambda d: "NPA" if d > 90 else "OK")` (vectorised `np.where` is faster).

### Q6. What are `map`, `filter`, `reduce`?
- `map(f, it)` applies f to each item: `list(map(str.upper, ["blr","mum"]))`.
- `filter(f, it)` keeps the items where f is True: `list(filter(lambda a: a["dpd"]>90, loans))`.
- `functools.reduce(f, it)` folds the items into one value: `reduce(lambda a,b: a+b, [1,2,3])` → 6.
- In interviews, say: "Comprehensions are usually more readable than map/filter in Python."

### Q7. What is scope? What is LEGB?
**Answer:** Python looks up names in **L**ocal → **E**nclosing → **G**lobal → **B**uilt-in order. Use `global` or `nonlocal` to assign to an outer variable (avoid it where you can).
- **Example 1:** A variable defined inside a function isn't visible outside it.
- **Example 2:** Naming your variable `list = [...]` shadows the built-in `list()`, which causes bugs later.

### Q8. What is a closure?
**Answer:** An inner function that remembers variables from its enclosing function even after the outer function has returned.
```python
def make_threshold_checker(limit):
    def check(amount): return amount > limit
    return check
is_high_value = make_threshold_checker(10_00_000)
is_high_value(15_00_000)  # True
```
- **Example 2:** `make_dpd_classifier(npa_days=90)` lets one client use 90 days and another use 180 (for some agri loans, by crop season).

### Q9. What is a decorator? Give a real example.
**Answer:** A function that takes a function and returns a new function that adds behaviour (logging, timing, retry, caching) without changing the original code. Syntax: `@decorator`.
```python
import time, functools
def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.perf_counter()-start:.2f}s")
        return result
    return wrapper

@timer
def load_loans(path): ...
```
- **Example 2, retry for LLM API calls (very relevant):**
```python
def retry(times=3, wait=2):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*a, **k):
            for attempt in range(1, times + 1):
                try:
                    return func(*a, **k)
                except Exception as e:
                    if attempt == times: raise
                    time.sleep(wait * attempt)   # backoff
        return wrapper
    return deco

@retry(times=3)
def call_claude(prompt): ...
```

### Q10. What is recursion? Example?
**Answer:** A function that calls itself on a smaller input until it reaches a base case. Python's default recursion limit is about 1000, so prefer loops for deep data.
- **Example 1:** Factorial: `def f(n): return 1 if n <= 1 else n * f(n-1)`.
- **Example 2:** Walk a nested JSON regulatory taxonomy to collect all leaf field names:
```python
def leaves(node, path=""):
    if isinstance(node, dict):
        for k, v in node.items():
            yield from leaves(v, f"{path}.{k}" if path else k)
    else:
        yield path
```

### Q11. `return` vs `print`? `return` vs `yield`?
**Answer:** `print` shows output. `return` gives a value back to the caller (a function without `return` returns None). `yield` makes the function a generator that produces values one by one and resumes from where it paused.
- **Example 1:** A function that only prints NPA counts can't be tested. Return the count instead.
- **Example 2:** `yield` chunks of a big PDF's text for embedding, one page at a time.

### Q12. What are type hints and docstrings?
**Answer:** Type hints document expected types. Python doesn't enforce them at runtime, but tools such as mypy and IDEs use them. Docstrings describe what a function does.
```python
def ecl(ead: float, pd_: float, lgd: float) -> float:
    """Expected Credit Loss = EAD x PD x LGD."""
    return ead * pd_ * lgd
```
- **Example 2:** Pydantic models use type hints to **validate** LLM JSON output (see GenAI files).

### Q13. What is `if __name__ == "__main__":`?
**Answer:** That code runs only when the file is executed directly, not when it's imported. It lets a file be both a module and a script.
- **Example 1:** `recon.py` has functions others import, plus a `main()` that runs recon when you call `python recon.py`.
- **Example 2:** A test file imports `clean_data()` without triggering the whole pipeline.

### Q14. What are pure functions and why do they matter for testing?
**Answer:** A pure function gives the same output for the same input and has no side effects (no file writes, no global changes). Pure functions are easy to unit-test.
- **Example 1:** `classify_dpd(95) == "NPA"` always holds, so it's easy to test.
- **Example 2:** Keep the LLM call (impure) separate from prompt building (pure), so you can unit-test the prompt template.
