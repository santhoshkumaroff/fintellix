# Evaluating GenAI Outputs (JD: "Evaluate the accuracy of Gen AI outputs through test cases and result comparisons")

> The JD names this explicitly. Fintellix clients are banks, and wrong output reaches regulators. Show that you **measure**, not just demo.

### Q1. Why is evaluating LLM output hard?
**Answer:** Outputs are free text, there can be many correct phrasings, they can vary between runs, and they can be confidently wrong. So you need defined criteria, test sets and a mix of automatic and human checks.
- **Example 1:** "NPA = overdue > 90 days" and "a loan turns non-performing after 90 days past due" are both correct but don't string-match.
- **Example 2:** The same prompt gives slightly different summaries on two runs. Your test must tolerate that.

### Q2. How do you build a test set (golden dataset)?
**Answer:** Collect realistic inputs with expected outputs, reviewed by a domain expert. Cover: common cases, edge cases, "answer not in the documents" cases, adversarial inputs, and each category or report type. Start with 30–100 and grow it from production failures.
| id | question | expected_answer | source_chunk | type |
|---|---|---|---|---|
| q1 | When is a loan NPA? | > 90 days overdue | c12 | definition |
| q2 | What is the capital of France? | Not in documents | — | out-of-scope |
| q3 | SMA-2 range? | 61–90 days | c33 | numeric |
- **Example 1:** 50 circular Q&As written with a compliance analyst.
- **Example 2:** 100 text-to-SQL questions with gold SQL from the data team.

### Q3. What metrics do you use?
| Task | Metric |
|---|---|
| Classification (complaint category) | Accuracy, precision, recall, F1, confusion matrix |
| Extraction (fields from documents) | Field-level exact match, % documents fully correct |
| Text-to-SQL | **Execution accuracy** (result sets match) |
| RAG retrieval | Recall@k, MRR |
| RAG answer | Correctness, faithfulness/groundedness, relevance, citation accuracy |
| Summaries | Coverage of key points, no unsupported claims, human rating |
| Ops | Latency, cost per query, failure/refusal rate |
- **Example 1:** Extraction across 200 loan agreements: `sanction_amount` 98.5% exact, `tenure` 96%. Tenure errors come from "months vs years", so fix the prompt.
- **Example 2:** Complaint classifier: CARD_FRAUD recall = 0.82. Missing fraud is costly, so prioritise improving recall.

### Q4. Precision vs recall vs F1 – explain with a banking example.
**Answer:** **Precision** = of the items flagged positive, how many really are. **Recall** = of the real positives, how many were caught. **F1** = their harmonic mean.
- **Example 1, fraud detection:** 100 real frauds. The model flags 80 transactions, 60 of them real frauds → precision 60/80 = 75%, recall 60/100 = 60%, F1 = 2·0.75·0.6/(1.35) ≈ 0.667.
- **Example 2, regulatory change tracker:** Missing a relevant circular (low recall) is worse than an extra false alert, so tune for high recall.

### Q5. What is LLM-as-a-judge? Its pros and cons?
**Answer:** A (usually strong) LLM grades outputs against a rubric, e.g. "Is the answer fully supported by the context? Score 1–5 with a reason." Pros: scalable, handles paraphrase. Cons: judge bias (it may prefer longer answers or its own style), cost, and it needs calibration against human labels.
```text
You are grading an answer for factual correctness.
Question: {q}
Reference answer: {ref}
Candidate answer: {ans}
Return JSON: {"correct": true/false, "reason": "..."}
Mark correct only if the candidate states the same facts as the reference; wording may differ.
```
- **Example 1:** Calibrate on 50 human-graded items. The judge agrees 92% of the time, which is acceptable.
- **Example 2:** Use a binary pass/fail with a clear rubric instead of a vague 1–10 score; it's more consistent.

### Q6. How do you compare results between two prompt/model versions? (JD: "result comparisons")
**Answer:** Run both versions on the **same test set**, compute metrics side by side, look at case-by-case differences (where A passed and B failed), check latency and cost, and only ship if the new version is better without regressions on critical cases.
```python
import pandas as pd
res = pd.DataFrame({"id": ids, "v1_correct": v1, "v2_correct": v2})
print(res[["v1_correct", "v2_correct"]].mean())     # accuracy per version
regressions = res[(res.v1_correct) & (~res.v2_correct)]
```
- **Example 1:** v2 accuracy 90% vs v1 85%, but v2 fails 2 numeric questions v1 got right. Investigate before shipping.
- **Example 2:** Claude Sonnet vs Haiku on complaint classification: Haiku costs a fraction and loses 1 point of accuracy, so use Haiku.

### Q7. How do you write automated tests for an LLM feature?
```python
# test_rag.py  (run: pytest -q)
import pytest, json
CASES = json.load(open("golden_set.json"))

@pytest.mark.parametrize("case", CASES, ids=lambda c: c["id"])
def test_answer(case):
    out = rag.answer(case["question"])
    if case["type"] == "out-of-scope":
        assert "could not find" in out.text.lower()
    else:
        assert case["source_chunk"] in out.sources            # citation correct
        assert judge(case["question"], case["expected"], out.text)   # semantic correctness
```
- **Example 2:** Deterministic checks first (JSON valid, required keys present, numbers match the source), then LLM-judge checks.

### Q8. How do you check faithfulness (no hallucination)?
**Answer:** Break the answer into claims and verify each against the retrieved context (with an NLI model or an LLM judge). Also check that every number in the answer appears in the context.
```python
import re
def numbers_grounded(answer: str, context: str) -> bool:
    nums = re.findall(r"\d+(?:\.\d+)?", answer)
    return all(n in context for n in nums)
```
- **Example 1:** The answer says "provision 15%" but the context says 25%. The numeric check flags it.
- **Example 2:** The answer cites chunk c12, but c12 doesn't mention the claim. Citation accuracy fails.

### Q9. What do you do after deployment? (monitoring)
**Answer:** Log inputs, retrieved sources, outputs, latency, cost and user feedback (thumbs up/down). Sample outputs for human review weekly. Add every failure to the golden set. Alert on spikes in "I don't know" answers or errors. Watch for drift when documents or models change.
- **Example 1:** A spike in "not found" answers after a new circular → it wasn't indexed.
- **Example 2:** Thumbs-down on 8% of SQL answers, mostly date questions → add date-handling examples to the prompt.

### Q10. Human-in-the-loop – where is it needed?
**Answer:** For high-impact outputs: anything submitted to a regulator, customer communication, mapping approvals, code changes. The LLM drafts, a human approves (maker-checker).
- **Example 1:** LLM-suggested source-to-target mappings are approved by the implementation consultant.
- **Example 2:** LLM-drafted variance commentary is edited and signed off by the finance lead.

### Q11. What would you report to your manager after an evaluation?
**Answer:** The test set size and composition, metrics per category, the top failure types with examples, cost and latency, a recommendation, and next steps.
- **Example:** "On 80 questions: correctness 88% (definitions 97%, tables 70%). Main failure: table extraction. Cost about ₹0.4 per query and p95 latency 3.1s. Recommend adding pdfplumber table parsing; expected gain about 8 points."
