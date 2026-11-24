# Explaining Your Project (JD: "At least one working Python or Gen AI project ... the candidate can explain in detail")

> Past candidates say Fintellix interviews **"mainly focus on the resume."** Your project is where you'll be tested hardest. Interviewers dig until you say "I don't know," and they want to see that you **built** it, not copied it.

## The 2-minute project pitch (memorise your version of this)
1. **Problem (15s):** Who has what pain?
2. **Solution (20s):** What you built, in one sentence.
3. **Architecture (30s):** The components and the flow (draw it).
4. **Tech stack (10s):** Language, libraries, model, vector DB, UI.
5. **Hard part (20s):** One real challenge and how you solved it.
6. **Results (15s):** Numbers: accuracy, time saved, test-set size.
7. **Next steps (10s):** What you'd improve.

**Example pitch (RegDoc Q&A, see the sample project file):**
> "Compliance teams read long RBI circulars to answer simple questions, which is slow and error-prone. I built a RAG chatbot that answers questions over RBI circulars with citations. PDFs are extracted with pypdf, split into section-aware chunks of about 600 tokens, embedded with all-MiniLM-L6-v2 and stored in FAISS. At query time I retrieve the top 4 chunks, and Claude answers only from them, citing chunk IDs, or says 'not found'. The hard part was table-heavy pages: plain text extraction scrambled them, so I extracted tables separately with pdfplumber as markdown chunks. On a 40-question golden set I wrote, retrieval Recall@4 is 92% and answer correctness is 85%, up from 70% before the table fix. Next I'd add hybrid BM25 search and a reranker."

---

## Deep-dive questions they WILL ask – prepare your own answers

### About the problem
1. Why did you choose this project? Who's the user?
2. What existed before? Why is your approach better?

### Architecture & design choices
3. Draw the architecture. Walk me through one request end to end.
4. Why this embedding model? What are its dimensions? Did you try others?
5. Why FAISS/Chroma and not X? What index type?
6. How did you chunk? Why that size and overlap? What happens at chunk boundaries?
7. How many chunks do you retrieve (k)? What if k is too high or too low?
8. Show me your prompt. Why is each line there?
9. Which LLM and why? What temperature? What max_tokens?
10. How do you handle "answer not in the documents"?

### Accuracy & evaluation (JD names this explicitly)
11. How do you know it works? What's your accuracy and how did you measure it?
12. How big is your test set and who made it?
13. Show me a failure case. Why did it fail? How did you fix it?
14. How do you detect hallucinations?

### Engineering
15. How do you handle API errors and rate limits?
16. Where do you store the API key?
17. What's the latency per query? Where's the time spent?
18. What does one query cost? How would you reduce it?
19. How would you scale to 100,000 documents? 1,000 concurrent users?
20. How do you update the index when a new document arrives?
21. Is it on GitHub? Show me the code structure. Do you have tests?

### Security / banking context
22. Could you use this with real bank data? What would you change? (PII masking, access control, on-premises or approved-region model, audit logs)
23. What if someone uploads a malicious document? (prompt injection)

### Reflection
24. What was the hardest bug?
25. What would you do differently?
26. What did you learn?

## Golden rules
- **Know your numbers** (chunk size, k, embedding dimensions, test-set size, accuracy, latency).
- **Be honest:** "I used LangChain's default splitter; I didn't tune it, but here's how I would." That beats bluffing.
- **Mention trade-offs.** It shows maturity.
- **Have the code ready** on GitHub with a clean README, a screenshot and an evaluation table.
- **Link it to Fintellix:** "This is the same pattern I'd apply to regulatory circulars or a Finbot-style text-to-SQL feature."

## Other project ideas that match this JD (if you need one fast)
| Project | Why it impresses Fintellix |
|---|---|
| **RAG over RBI circulars with citations + eval** | Directly their domain |
| **Text-to-SQL bot on a loan database (mini-Finbot)** | Mirrors their actual product |
| **Bank statement / invoice PDF → structured Excel with LLM + validation** | Automation + extraction + evaluation |
| **Automated reconciliation + LLM commentary** | Python automation + GenAI explanation |
| **Complaint classifier with LLM vs classical ML comparison** | Evaluation skills |
| **Column-mapping assistant (source → standard schema)** | Matches the data-model implementation work |
