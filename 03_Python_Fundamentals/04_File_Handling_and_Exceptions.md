# File Handling, Exceptions, Modules (JD: "file handling")

### Q1. How do you read and write files in Python?
**Answer:** Use `open(path, mode, encoding=...)` inside a `with` block, which closes the file automatically, even on errors. Modes: `r` read, `w` write (overwrites), `a` append, `x` create-only, `b` binary, `+` read/write.
```python
with open("loans.txt", "r", encoding="utf-8") as f:
    for line in f:              # memory-efficient, line by line
        print(line.strip())

with open("errors.log", "a", encoding="utf-8") as f:
    f.write("L001: negative balance\n")
```
- **Example 2:** Write a PDF in binary mode: `open("out.pdf", "wb").write(response.content)`.

### Q2. Why use `with`? What is a context manager?
**Answer:** A context manager runs setup and cleanup code (`__enter__` / `__exit__`). `with` guarantees cleanup: closing files, releasing DB connections, unlocking.
- **Example 1:** `with sqlite3.connect("bank.db") as conn:` commits the transaction on success and rolls it back if an exception is raised. Note that it doesn't close the connection; call `conn.close()` for that.
- **Example 2, custom timer:**
```python
from contextlib import contextmanager
import time
@contextmanager
def timed(label):
    t = time.perf_counter(); yield; print(label, time.perf_counter() - t)
with timed("embedding"): ...
```

### Q3. `read()` vs `readline()` vs `readlines()`?
**Answer:** `read()` returns the whole file as one string. `readline()` returns one line. `readlines()` returns a list of all lines. For big files, iterate `for line in f`.
- **Example 1:** A small prompt template file: `template = f.read()`.
- **Example 2:** A 5 GB transaction log: `for line in f` to avoid running out of memory.

### Q4. How do you work with CSV and JSON?
```python
import csv, json
with open("loans.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):          # each row is a dict
        print(row["loan_id"], row["dpd"])

with open("config.json") as f: cfg = json.load(f)        # file -> dict
with open("out.json", "w") as f: json.dump(cfg, f, indent=2)
data = json.loads('{"a": 1}')                              # string -> dict
```
- **Example 1:** Load regulator validation rules from a JSON config.
- **Example 2:** Parse an LLM's JSON output with `json.loads(response_text)` inside try/except.

### Q5. How do you read Excel and PDF files?
- Excel: `pd.read_excel("returns.xlsx", sheet_name="NPA")` (needs openpyxl); `pd.read_excel(path, sheet_name=None)` returns all sheets as a dict.
- PDF text: `pypdf` (`PdfReader(path).pages[i].extract_text()`) or `pdfplumber` for tables.
- **Example 1:** Load 12 monthly Excel returns and concatenate them.
- **Example 2:** Extract text from RBI circular PDFs for a RAG pipeline.

### Q6. How do you handle file paths safely across OSes?
**Answer:** Use `pathlib.Path`.
```python
from pathlib import Path
base = Path("data") / "2026" / "Q3"
for csv_file in base.glob("*.csv"): print(csv_file.name, csv_file.stat().st_size)
base.mkdir(parents=True, exist_ok=True)
```
- **Example 2:** `Path("report.csv").with_suffix(".xlsx")` to build an output name.

### Q7. What is exception handling? try / except / else / finally?
**Answer:** Exception handling catches runtime errors so the program can recover or fail cleanly.
- `try`: risky code. `except`: handle a specific error. `else`: runs if no error. `finally`: always runs (cleanup).
```python
try:
    amount = float(row["amount"])
except ValueError:
    log_bad_row(row, "amount not numeric")
    amount = None
else:
    total += amount
finally:
    processed += 1
```
- **Example 2:** Wrap the LLM API call: catch rate-limit and timeout errors, retry, and log anything else.

### Q8. Why catch specific exceptions instead of bare `except:`?
**Answer:** A bare `except` hides bugs (even typos and KeyboardInterrupt). Catch only the errors you expect and can handle.
- **Example 1:** `except FileNotFoundError:` → "Client file for March missing", plus an alert.
- **Example 2:** `except json.JSONDecodeError:` → ask the LLM again for valid JSON.

### Q9. Common built-in exceptions?
`ValueError`, `TypeError`, `KeyError`, `IndexError`, `FileNotFoundError`, `ZeroDivisionError`, `AttributeError`, `ImportError`, `json.JSONDecodeError`.
- **Example 1:** `{"a":1}["b"]` → KeyError (use `.get("b")`).
- **Example 2:** NPA% when total advances = 0 → ZeroDivisionError. Guard it: `npa / total if total else 0`.

### Q10. How do you raise and create custom exceptions?
```python
class ValidationError(Exception):
    """Raised when a regulatory validation rule fails."""

def check_balance(bal):
    if bal < 0:
        raise ValidationError(f"Negative balance: {bal}")
```
- **Example 2:** `class LLMOutputError(Exception)` when the model's answer doesn't match the expected schema.

### Q11. What is logging and why not just print?
**Answer:** `logging` gives levels (DEBUG, INFO, WARNING, ERROR, CRITICAL), timestamps and file output, and you can switch it off in production. Logs are an audit trail, which banks need.
```python
import logging
logging.basicConfig(filename="pipeline.log", level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")
logging.info("Loaded %d rows", 10000)
logging.error("Recon break of %.2f in product %s", 1200.5, "HOME")
```
- **Example 2:** Log every LLM prompt ID, token count and latency (never the raw customer PII).

### Q12. Modules vs packages? How does import work?
**Answer:** A module is a `.py` file. A package is a folder of modules (traditionally with `__init__.py`). `import x` searches `sys.path`.
- **Example 1:** `from utils.cleaning import clean_columns`.
- **Example 2:** Install third-party packages with `pip install pandas`, pin them in `requirements.txt`, and isolate them with `python -m venv .venv`.

### Q13. What is a virtual environment and why use it?
**Answer:** An isolated Python environment per project, so dependency versions don't clash.
- **Example 1:** Project A needs `langchain==0.2`, project B needs `0.3`. Separate venvs avoid conflicts.
- **Example 2:** `pip freeze > requirements.txt` lets a teammate reproduce your setup exactly.

### Q14. How do you keep secrets (API keys) out of code?
**Answer:** Use environment variables or a `.env` file (loaded with `python-dotenv`), add `.env` to `.gitignore`, and never commit keys. In production, use a secrets manager.
```python
import os
api_key = os.environ["ANTHROPIC_API_KEY"]   # KeyError if missing – fail fast
```
- **Example 2:** If a key is accidentally pushed to GitHub, **revoke it immediately**. Deleting the commit isn't enough.
