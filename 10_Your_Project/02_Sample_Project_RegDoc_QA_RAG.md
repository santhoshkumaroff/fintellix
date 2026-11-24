# Sample Project: RegDoc Q&A – RAG Chatbot over Regulatory Documents

> Working code is in `regdoc_qa_code/`. It was tested in this kit: retrieval scores 8/8 (Recall@2) on the included golden set using the offline TF-IDF fallback. **Build it, run it, break it, and fix it yourself.** An interviewer can tell within 2 questions whether you built a project or only read about it.

## 1. Problem
Compliance and reporting teams search long regulator circulars to answer simple questions ("What is SMA-2?", "What is the minimum LCR?"). It's slow, and people misread clauses.

## 2. Solution
A chatbot that answers **only from the documents**, cites the chunk it used, and says "not found" when the answer isn't in the documents.

## 3. Architecture
```
docs/ (PDF/TXT)  ->  load_documents()  ->  build_chunks()  ->  Retriever (MiniLM+FAISS, or TF-IDF fallback)
                                                                         |
question --------------------------------------------------------------> search(top-k)
                                                                         |
                                                     build_prompt(question, chunks) + SYSTEM_RULES
                                                                         |
                                                                 Claude (temperature 0)
                                                                         |
                                                        answer + "Sources: [c2]"  +  retrieved ids/scores
```

## 4. How to run
```bash
cd regdoc_qa_code
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-...                         # never commit this
python rag.py --eval                                    # retrieval evaluation on golden_set.json
python rag.py --ask "What is SMA-1?" --no-llm           # see retrieved chunks only
python rag.py --ask "What is SMA-1?"                    # full answer from Claude
```
Then **replace `docs/sample_regulatory_notes.md` with 5–10 real RBI circular PDFs** from rbi.org.in, and **extend `eval/golden_set.json` to 30–40 questions** you write yourself. That makes it *your* project with *your* numbers.

## 5. Key design decisions (be ready to defend each)
| Decision | Choice | Why | Alternative |
|---|---|---|---|
| Chunking | Paragraph-aware, ~120 words, 20-word overlap | Regulatory text is organised by paragraph; overlap keeps context | Fixed tokens, by heading, RecursiveCharacterTextSplitter |
| Embeddings | all-MiniLM-L6-v2 (384-dim) | Free, fast, runs on CPU, decent quality | bge-base, e5, Voyage (higher quality, cost/size) |
| Index | FAISS IndexFlatIP on normalised vectors | Exact cosine search; fine below ~100k chunks | HNSW for scale, Chroma for metadata filters |
| Fallback | TF-IDF | Works offline; good for exact terms like "SMA-1" | Hybrid of both (best) |
| k | 4 | Enough recall without diluting the prompt | Tune on the eval set |
| LLM | Claude, temperature 0 | Strong instruction following and grounding; deterministic-ish | A smaller model for cost |
| Prompt | "ONLY context", exact "not found" phrase, cite ids | Reduces hallucination; testable refusal | — |
| Evaluation | Golden set + Recall@k + answer checks | JD asks for test cases and result comparisons | RAGAS, LLM-as-judge |

## 6. Walk through the code (they may ask "explain this function")
- `load_documents`: reads .txt/.md directly and .pdf with pypdf, one dict per document with `source` for citations.
- `chunk_document`: splits on blank lines (paragraphs), accumulates up to `max_words`, carries over the last 20 words as overlap.
- `Retriever.__init__`: tries sentence-transformers + FAISS. If the import fails, it falls back to TF-IDF (graceful degradation).
- `search`: encodes the query the same way as the docs (**must use the same model**), returns the top-k chunks with scores.
- `build_prompt`: wraps the chunks in `<context>` with `[id] (source)` prefixes so the model can cite them.
- `ask_claude`: Messages API call with `system=SYSTEM_RULES`, `temperature=0`, `max_tokens=500`.
- `evaluate_retrieval`: for each golden question, checks that the retrieved text contains the expected keywords, then prints Recall@k.

## 7. Experiments to run (then talk about them)
1. Change `-k` from 1 → 2 → 4 and record Recall@k.
2. Change chunk size from 60 → 120 → 300 words and see what happens to recall.
3. Ask an out-of-scope question ("What is the repo rate?") and confirm it says "not found."
4. Ask a paraphrased question ("after how many overdue days is a loan bad?"). TF-IDF may fail where embeddings succeed. **That's a great interview story about keyword vs semantic search.**
5. Add a hybrid score: `0.5 * tfidf + 0.5 * embedding`.

## 8. Interview Q&A on this project
### Q1. Why not just send the whole document to Claude?
**Answer:** For one short document you could. With hundreds of circulars, it costs more, runs slower, exceeds the context window, and gives less precise citations. RAG sends only the relevant ~4 chunks.
- **Example 1:** 200 circulars ≈ 5M tokens, which can't go in one prompt.
- **Example 2:** One 10-page circular with a long-context model is fine, so I'd use direct prompting there.

### Q2. How do you stop it from hallucinating?
**Answer:** A strict system prompt (only the context, an exact "not found" phrase), temperature 0, citations required, an evaluation set that includes out-of-scope questions, and an optional check that the numbers in the answer appear in the retrieved text.
- **Example 1:** "What is the repo rate?" → "I could not find this in the provided documents."
- **Example 2:** The numeric check flags an answer with "180 days" when the context only says 90.

### Q3. How would you make it production-ready for a bank?
**Answer:** Real PDF and table parsing, metadata (circular no, date, active version), hybrid search + reranker, access control, PII masking, logging and audit, a FastAPI service + UI, CI with the golden-set evaluation, monitoring with user feedback, and an approved model hosting arrangement (e.g. a cloud region the bank approves).
- **Example 1:** Add `is_active` metadata so superseded circulars aren't retrieved.
- **Example 2:** Run the evaluation in GitHub Actions on every PR.

### Q4. What was the hardest part?
**Prepare your own true story.** Common real ones: PDF tables scrambled into text; chunk boundaries splitting a definition in half (fixed with overlap or paragraph chunking); paraphrased questions failing with keyword search (fixed with embeddings or hybrid); the model answering from general knowledge instead of the document (fixed with stricter instructions and an exact refusal phrase).

### Q5. How would you turn this into a Finbot-style feature?
**Answer:** Add a router: if the question is about **rules or definitions**, use RAG. If it's about **numbers in the data** ("NPA in MUM last month"), use text-to-SQL on a read-only database, run the query, and let Claude explain the result. Evaluate each path separately.
