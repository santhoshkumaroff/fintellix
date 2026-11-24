# Automation with Python (JD: "Automate manual and repetitive tasks using Python and AI-assisted tools, and support the team on client implementation projects")

### Q1. How do you identify what to automate?
**Answer:** Look for tasks that are **repetitive, rule-based, frequent, time-consuming and error-prone**. Estimate time saved = (minutes per run × runs per month) and weigh it against the build effort. Start with the biggest pain point.
- **Example 1:** An analyst spends 2 hours every month copying 12 branch Excel files into one sheet. A 30-line pandas script does it in 10 seconds.
- **Example 2:** Comparing source vs report totals by hand for 40 products → an automated reconciliation report with highlighted breaks.

### Q2. Describe an automation you built (or would build). (STAR format)
**Answer template:** **S**ituation (the manual pain) → **T**ask → **A**ction (tools, logic, edge cases) → **R**esult (time saved, errors reduced, adoption).
- **Example 1:** "My college placement cell merged 30 Google Form CSVs by hand every week. I wrote a Python script that downloads, cleans, deduplicates and outputs one Excel with pivot summaries. Time went from 3 hours to 2 minutes, with zero copy-paste errors."
- **Example 2:** "I built an LLM script that reads 200 PDF invoices and extracts vendor, date and amount to Excel. I validated it on 30 invoices against manual entry: 97% field accuracy. Failures were handwritten dates, which I flagged for manual review."

### Q3. Script: merge all Excel/CSV files in a folder
```python
from pathlib import Path
import pandas as pd

def merge_folder(folder: str, out: str):
    frames = []
    for f in sorted(Path(folder).glob("*.xlsx")):
        df = pd.read_excel(f)
        df["source_file"] = f.name          # lineage!
        frames.append(df)
    merged = pd.concat(frames, ignore_index=True)
    merged.to_excel(out, index=False)
    print(f"Merged {len(frames)} files, {len(merged)} rows -> {out}")

merge_folder("branch_files/2026-10", "consolidated_oct.xlsx")
```
- **Example 2:** The same pattern with `*.csv` and `pd.read_csv`, plus a check that every file has the same columns.

### Q4. Script: automated reconciliation report
```python
import pandas as pd
src = pd.read_csv("core_banking.csv")    # account_id, balance
rpt = pd.read_csv("report_data.csv")     # account_id, balance

m = src.merge(rpt, on="account_id", how="outer", suffixes=("_src", "_rpt"), indicator=True)
m["diff"] = m["balance_src"].fillna(0) - m["balance_rpt"].fillna(0)
m["status"] = "MATCH"
m.loc[m["_merge"] == "left_only", "status"] = "MISSING_IN_REPORT"
m.loc[m["_merge"] == "right_only", "status"] = "MISSING_IN_SOURCE"
m.loc[(m["_merge"] == "both") & (m["diff"].abs() > 0.01), "status"] = "AMOUNT_MISMATCH"

summary = m.groupby("status").agg(count=("account_id", "count"), diff=("diff", "sum"))
with pd.ExcelWriter("recon_report.xlsx") as w:
    summary.to_excel(w, sheet_name="Summary")
    m[m.status != "MATCH"].to_excel(w, sheet_name="Breaks", index=False)
```
- **Example 2:** Schedule it daily and email the ops team only when breaks exist.

### Q5. Script: validation rules engine driven by config
```python
RULES = [
    {"id": "R1", "desc": "Outstanding not negative", "expr": "outstanding < 0"},
    {"id": "R2", "desc": "DPD>90 must be NPA",       "expr": "dpd > 90 and npa_flag != 'Y'"},
    {"id": "R3", "desc": "Rate between 0 and 36",    "expr": "interest_rate < 0 or interest_rate > 36"},
]
def run_rules(df):
    results = []
    for r in RULES:
        bad = df.query(r["expr"])
        results.append({"rule": r["id"], "desc": r["desc"], "failed": len(bad)})
        if len(bad):
            bad.assign(rule=r["id"]).to_csv(f"fail_{r['id']}.csv", index=False)
    return pd.DataFrame(results)
```
- **Why config-driven:** new rules don't need code changes. This is the same idea as Fintellix's configurable validation framework.
- **Example 2:** Store the rules in a YAML file that business analysts can edit.

### Q6. How do you schedule a Python job?
**Answer:** Linux **cron**, Windows Task Scheduler, or orchestrators such as Airflow, Prefect or cloud schedulers. Add logging, alerts on failure, and idempotency.
```bash
# crontab -e   -> run every day at 7:30 AM
30 7 * * * /home/user/.venv/bin/python /home/user/recon/run_recon.py >> /home/user/recon/cron.log 2>&1
```
- **Example 2:** Airflow DAG: extract → validate → transform → report, with retries and an email on failure.

### Q7. How do you send an automated email with an attachment?
```python
import smtplib, os
from email.message import EmailMessage
msg = EmailMessage()
msg["Subject"] = "Daily Recon – 3 breaks"
msg["From"], msg["To"] = "bot@company.com", "ops@company.com"
msg.set_content("Please find the recon report attached.")
with open("recon_report.xlsx", "rb") as f:
    msg.add_attachment(f.read(), maintype="application",
                       subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                       filename="recon_report.xlsx")
with smtplib.SMTP("smtp.company.com", 587) as s:
    s.starttls(); s.login("bot@company.com", os.environ["SMTP_PASS"]); s.send_message(msg)
```
- **Example 2:** Post to a Teams or Slack webhook with `requests.post(url, json={...})`.

### Q8. How do you automate with an LLM in the loop? (GenAI automation)
**Answer:** Use Python for the deterministic parts (read, loop, validate, write) and the LLM for the fuzzy text parts (understand, extract, summarise, classify). Always validate the LLM output and route low-confidence cases to a human.
```python
results = []
for path in Path("circulars").glob("*.pdf"):
    text = extract_text(path)
    summary = ask_claude_json(SUMMARY_PROMPT.format(text=text[:50000]))   # returns validated Pydantic object
    results.append({"file": path.name, **summary.model_dump()})
pd.DataFrame(results).to_excel("circular_tracker.xlsx", index=False)
```
- **Example 1:** A weekly regulatory-change digest: download new circulars → summarise → classify relevance → email.
- **Example 2:** Implementation support: the LLM suggests column mappings for a new client file, the consultant approves them in Excel, and the script applies the approved mapping.

### Q9. How do you automate web or API data collection?
**Answer:** Use APIs when available (`requests`, with auth, pagination and retries). Scrape only when allowed (check the terms and robots.txt) with BeautifulSoup. Use Selenium or Playwright for dynamic pages. Respect rate limits.
- **Example 1:** Pull daily FX rates from an official API to revalue foreign-currency balances.
- **Example 2:** Download new circular PDFs from a regulator's publications page (if permitted).

### Q10. How do you make automation robust?
**Answer:** Input validation, clear error messages, logging, retries for network calls, idempotent runs, config files instead of hard-coding, unit tests, a dry-run mode, and documentation (a README).
- **Example 1:** If the input file is missing, log an error and alert the owner. Don't silently produce an empty report.
- **Example 2:** Re-running the job for the same date overwrites that date's output rather than duplicating it.

### Q11. How do you automate Excel formatting?
**Answer:** Use `openpyxl` or `xlsxwriter` for formats, conditional highlighting, column widths and formulas.
```python
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
wb = load_workbook("recon_report.xlsx"); ws = wb["Breaks"]
red = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
for row in ws.iter_rows(min_row=2):
    if row[-1].value == "AMOUNT_MISMATCH":
        for c in row: c.fill = red
wb.save("recon_report.xlsx")
```

### Q12. What is RPA and how is Python automation different?
**Answer:** RPA (UiPath, Automation Anywhere) mimics UI clicks. It's good for legacy apps without APIs, but fragile when screens change. Python automation works on data and APIs directly, so it's more robust and testable. GenAI adds handling of unstructured inputs.
- **Example:** Logging into an old portal to download a report → RPA or Playwright. Processing the downloaded file → Python.
