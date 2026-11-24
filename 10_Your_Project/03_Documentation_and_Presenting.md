# Documenting & Presenting Work (JD: "Document work and present learnings to the team")

### Q1. How do you document your code and projects?
**Answer:** README (purpose, setup, how to run, examples, limitations), docstrings and type hints, comments that explain **why** rather than what, a config reference, architecture diagrams, a changelog, and evaluation results.
- **Example 1:** README sections: Problem → Architecture diagram → Setup → Usage → Evaluation table → Known limitations → Next steps.
- **Example 2:** A one-page "runbook" for the recon script: inputs, schedule, what to do when it fails, the owner.

### Q2. How would you present a technical learning to a non-technical team?
**Answer:** Start with the business problem and the outcome, use simple analogies, show a live demo or screenshot, give one number that matters, keep the jargon minimal, and end with what you need from them.
- **Example 1:** "RAG is like an open-book exam: the AI looks up the right page in our circulars before answering, and shows you which page."
- **Example 2:** "This script cut the monthly consolidation from 3 hours to 2 minutes, and there have been no copy-paste errors since."

### Q3. How would you structure a 10-minute presentation of your internship work?
1. Problem and why it matters (1 min)
2. What I built: a demo (3 min)
3. How it works: one diagram (2 min)
4. Results: accuracy, time saved (2 min)
5. Limitations and next steps (1 min)
6. Questions (1 min)

### Q4. How do you write a good technical summary or email to your manager?
**Answer:** Bottom line first, then supporting points, then asks or blockers. Keep it short.
- **Example:**
  > **Status:** RAG evaluation done – 88% correct on 80 questions.
  > **Main gap:** table questions (70%). Fix: table-aware parsing, ETA Thursday.
  > **Need:** 20 more real questions from the compliance team.

### Q5. What do you do when you don't understand something during training?
**Answer:** Try first (docs, code, search) with a time box, then ask a specific question that shows what I already tried, and write down the answer so I don't ask twice.
- **Example 1:** "I traced the NPA flag to the `asset_class` column, but I don't see where SMA buckets are computed. Is that in the rule engine config?"
- **Example 2:** Keep a personal "domain glossary" document while learning regulatory terms.
