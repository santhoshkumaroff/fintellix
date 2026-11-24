# RAG – Retrieval-Augmented Generation (JD: "RAG workflows") — MOST IMPORTANT FILE

### Q1. What is RAG? Explain simply.
**Answer:** RAG = **retrieve** relevant information from your own documents, then **augment** the prompt with it, so the LLM **generates** an answer grounded in that information. It's like an open-book exam: the model looks up the right pages before answering.
- **Example 1:** An employee asks "What is the provisioning rate for substandard assets?" The system finds the paragraph in the RBI master direction and Claude answers with a citation.
- **Example 2:** A Fintellix implementation consultant asks "How is field X mapped for client Y?" RAG over the project documentation answers instantly.

### Q2. Why RAG? What problems does it solve?
**Answer:** (1) The LLM doesn't know private or recent data. (2) It reduces hallucination by grounding answers. (3) It gives **citations** for auditability. (4) You update knowledge by re-indexing, with no retraining. (5) Access control at retrieval time.
- **Example 1:** New circular this morning → index it → the bot knows it in minutes.
- **Example 2:** The auditor asks "where did this answer come from?" → the cited chunk and document link.

### Q3. Draw the RAG architecture. (whiteboard question)
```
INDEXING (offline)
Documents (PDF/HTML/Docx) -> Load/Extract text -> Clean -> Chunk (+metadata)
     -> Embed each chunk -> Store in Vector DB

QUERY (online)
User question -> (optional: rewrite query) -> Embed question
     -> Vector/Hybrid search (top-k, metadata filters) -> (optional: rerank)
     -> Build prompt: instructions + retrieved chunks + question
     -> LLM (e.g. Claude) -> Answer + citations -> (optional: guardrail/validation) -> User
```
- **Example 1:** Indexing runs nightly over the circular repository. Queries run in real time.
- **Example 2:** In a chat, also include the last few turns so follow-ups like "and for doubtful assets?" work.

### Q4. Walk through each step in detail.
1. **Load:** `pypdf`/`pdfplumber` for PDFs, BeautifulSoup for HTML, OCR (Tesseract) for scans.
2. **Clean:** remove headers and footers, page numbers, broken hyphenation.
3. **Chunk:** by section or paragraph, ~300–800 tokens, 10–20% overlap. Keep headings.
4. **Metadata:** `source, title, circular_no, date, page, section, regulator, version`.
5. **Embed:** with an embedding model. Store the vector + text + metadata.
6. **Retrieve:** top-k (3–10) by cosine similarity. Combine with keyword search (hybrid). Filter by metadata.
7. **Rerank:** a cross-encoder picks the best few.
8. **Generate:** a prompt with strict grounding rules, then the LLM.
9. **Post-process:** check that citations exist, format the answer, log everything.

### Q5. What prompt do you use for the generation step?
```text
You are an assistant for banking regulatory questions.
Use ONLY the information in <context>. Each chunk has an id.
If the context does not contain the answer, say: "I could not find this in the provided documents."
Do not use outside knowledge. Quote numbers exactly as written.
After the answer, list the chunk ids you used as: Sources: [id1, id2]

<context>
[c12] (RBI Master Direction, para 4.2.1) A non-performing asset (NPA) is a loan ...
[c47] (RBI Master Direction, para 5.1) Banks shall make a general provision ...
</context>

Question: {question}
```
- **Example 2:** For a business user, add "Explain in simple language in under 120 words."

### Q6. What are common RAG failure modes and fixes? (very likely question)
| Problem | Cause | Fix |
|---|---|---|
| Right info not retrieved | Bad chunking, weak embeddings, vocabulary mismatch | Structure-aware chunks, hybrid search, query rewriting, a better model |
| Retrieved but the answer is wrong | Too many irrelevant chunks, "lost in the middle" | Reranking, fewer but better chunks, put the best chunks first or last |
| Hallucinated answer | Weak instructions | Strict "only from context" + "I don't know" + citation check |
| Outdated answer | Old versions indexed | Version/date metadata, filter active docs |
| Tables answered badly | PDF table text scrambled | Table-aware extraction (pdfplumber, camelot), store tables as markdown |
| Slow / costly | Too much context | Smaller k, caching, cheaper model for simple questions |
- **Example 1:** The question "What is SMA-1?" retrieved a chunk about "SMA reporting to CRILC" instead of the definition. Adding BM25 hybrid search fixed it, because the definition contains the exact term "SMA-1".
- **Example 2:** Answers quoted a 2019 rule that had been superseded. Filtering `is_active=True` fixed it.

### Q7. What is "lost in the middle"?
**Answer:** LLMs tend to use information at the start and end of a long context better than information in the middle. So put the most relevant chunks first (or last), and don't stuff 30 chunks in.
- **Example:** With 20 chunks, the correct one at position 10 got ignored. Reranking it to position 1 fixed the answer.

### Q8. What are advanced RAG techniques?
- **Query rewriting / expansion:** the LLM rewrites a vague question into a better search query, or several queries.
- **HyDE:** generate a hypothetical answer, embed it, and search with that.
- **Multi-query:** search several rephrasings and merge the results.
- **Parent-child (small-to-big) retrieval:** match on small chunks, send the larger parent section to the LLM.
- **Contextual retrieval:** prepend a short document-level context to each chunk before embedding (Anthropic published this technique).
- **Hybrid search + reranking.**
- **GraphRAG:** a knowledge graph of entities and relations for multi-hop questions.
- **Agentic RAG:** the LLM decides when and what to retrieve, possibly in several steps.
- **Example 1:** "What changed between the 2023 and 2025 versions of the KYC direction?" → agentic RAG retrieves both versions and compares them.
- **Example 2:** "Which reports are affected by the new definition of 'exposure'?" → GraphRAG links definition → reports.

### Q9. How do you evaluate a RAG system? (JD: "Evaluate the accuracy of Gen AI outputs")
**Answer:** Evaluate **retrieval** and **generation** separately, on a **golden dataset** of questions with expected answers and source chunks.
- **Retrieval:** Recall@k, MRR.
- **Generation:**
  - **Faithfulness / groundedness:** is every claim supported by the retrieved context?
  - **Answer relevance:** does it answer the question?
  - **Correctness:** does it match the expected answer?
  - **Citation accuracy:** do the cited chunks actually contain the claim?
- **Tools:** RAGAS, DeepEval, TruLens, LangSmith, or your own pytest plus LLM-as-judge.
- **Example 1:** 60 golden Q&As on RBI NPA rules: Recall@5 = 93%, correctness = 87%, faithfulness = 95%. Failures were mostly table questions, so table extraction comes next.
- **Example 2:** Regression test: every prompt change re-runs the 60 questions in CI. If correctness drops more than 2 points, the change is blocked.

### Q10. How do you handle tables and numbers in RAG?
**Answer:** Extract tables separately and keep them as markdown or CSV chunks with captions. For data that is fundamentally tabular (loan tables), use **text-to-SQL** instead of embedding rows. Never let the LLM compute aggregates from many rows. Let SQL or pandas do it.
- **Example 1:** A provisioning-percentage table from a circular is stored as one markdown chunk with the caption "Provisioning requirements by asset class".
- **Example 2:** "Total NPA in Karnataka?" → SQL query, not RAG.

### Q11. RAG vs long context – do we still need RAG?
**Answer:** Yes, usually. RAG is cheaper per query, faster, scales to millions of documents, gives precise citations, and enforces access control. Long context is useful for deep analysis of one or a few documents. They combine well: retrieve the relevant docs, then send whole sections.
- **Example 1:** 10,000 circulars → RAG.
- **Example 2:** Compare two versions of one 60-page circular → long context with both versions in full.

### Q12. How do you add conversation memory to a RAG chatbot?
**Answer:** Keep the recent turns. For a follow-up, **condense** the history plus the new question into a standalone question before retrieval.
- **Example:** History: "What is SMA-1?" New: "and SMA-2?" → rewritten to "What is the definition of SMA-2?" → retrieve.

### Q13. How do you secure a RAG system in a bank?
**Answer:** Document-level access control (filter by user permissions at retrieval), PII masking, an approved model hosting location, audit logs of question + retrieved chunks + answer, prompt-injection defences (treat documents as untrusted), and rate limits.
- **Example 1:** An HR policy document is visible only to the HR group, so filter `allowed_groups` contains the user's group.
- **Example 2:** Store a hash of every answer and its sources for audit replay.

### Q14. Minimal RAG code (know every line)
See the full runnable project in `10_Your_Project/02_Sample_Project_RegDoc_QA_RAG.md`. Core idea:
```python
def answer(question, k=4):
    q_vec = embedder.encode([question], normalize_embeddings=True).astype("float32")
    scores, ids = index.search(q_vec, k)
    context = "\n\n".join(f"[{chunks[i]['id']}] {chunks[i]['text']}" for i in ids[0])
    prompt = f"<context>\n{context}\n</context>\n\nQuestion: {question}"
    msg = client.messages.create(
        model="claude-sonnet-5-5", max_tokens=500, temperature=0,
        system=SYSTEM_RULES,
        messages=[{"role": "user", "content": prompt}])
    return msg.content[0].text
```

### Q15. What is text-to-SQL and how is it related? (Finbot-style)
**Answer:** The LLM converts a natural-language question into SQL using the schema (and sometimes sample rows and business definitions). The SQL runs on the database, and the result is returned or explained. It's like RAG, but the "retrieval" is a database query.
**Safety:** read-only user, whitelist of tables, SELECT-only check, row limits, show the SQL to the user, validate against known queries.
- **Example 1:** "Top 5 branches by NPA amount last month" →
```sql
SELECT branch, SUM(outstanding) AS npa_amt
FROM loans WHERE dpd > 90 AND snapshot_month = '2026-10'
GROUP BY branch ORDER BY npa_amt DESC LIMIT 5;
```
- **Example 2:** Evaluation: 100 questions with gold SQL. Compare **result sets** (execution accuracy), not SQL strings, because different SQL can give the same correct result.
