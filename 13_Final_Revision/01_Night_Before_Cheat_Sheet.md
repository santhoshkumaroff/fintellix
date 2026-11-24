# Night-Before Cheat Sheet (read this 1 hour before the interview)

## Company in 3 lines
- **Fintellix**: Bengaluru RegTech/SupTech company, founded 2006, part of **Group ICRA** (ICRA completed the acquisition on 17 Oct 2025; Moody's is ICRA's largest shareholder).
- Platform: **Data Curation + Data Analytics** platforms → solutions: **Regulatory Reporting** (RBI, CBUAE, SAMA, CBK, BoM, MAS, HKMA, APRA, FCS, UK, US CECL/CCAR), **Credit Risk** (NPA, EWS, ECL), **Syndicate Reporting** (Lloyd's), **Supervisory** platforms for regulators.
- AI: **Finbot** (conversational data insights through SQL) and an **AI Compliance Tracker**. Claims "$9 Tr+ assets reported."

## Domain in 10 terms
NPA = >90 days overdue | SMA-0/1/2 = 1–30/31–60/61–90 | GNPA vs NNPA (minus provisions) | PCR = provisions/GNPA | ECL = PD×LGD×EAD, Stages 1/2/3 | CRAR = capital/RWA | LCR = HQLA/30-day outflows ≥100% | BCBS 239 = risk data aggregation principles | XBRL → RBI **CIMS** | maker-checker + data lineage.

## Python in 10 lines
list (mutable) / tuple (immutable, hashable) / set (unique, O(1) lookup) / dict (hash map) • shallow vs deep copy • `is` vs `==` • comprehensions & generators (`yield`, lazy) • `*args/**kwargs` • mutable default trap (`None`) • decorators (timer/retry) • OOP: encapsulation, abstraction, inheritance, polymorphism; `@classmethod`/`@staticmethod`; dataclass • `with open()` context manager • specific exceptions + logging • GIL: threads for I/O (API calls), processes for CPU • `Decimal` for money.

## Pandas in 10 calls
`read_csv(parse_dates)`, `info/describe/isna().sum()`, `loc` vs `iloc`, boolean filters with `&`/`|`, `fillna/dropna` (flag; never silently fill regulatory fields), `drop_duplicates(subset)`, `groupby().agg(named)`, `merge(how, indicator=True)` for recon, `pivot_table`, `np.where/np.select` instead of `apply`, `read_csv(chunksize)` for big files.

## SQL in 8 lines
JOIN types (anti-join = LEFT + IS NULL) • WHERE (rows) vs HAVING (groups) • execution order FROM→WHERE→GROUP BY→HAVING→SELECT→ORDER BY→LIMIT • CASE WHEN buckets • subquery (correlated vs not), NOT EXISTS over NOT IN • CTE • ROW_NUMBER/RANK/DENSE_RANK/LAG • parameterised queries against injection.

## DW in 5 lines
OLTP vs OLAP • ETL vs ELT • fact (measures + FKs) vs dimension (context) • star (denormalised) vs snowflake • SCD Type 1 (overwrite) vs Type 2 (new row + valid_from/to) • grain • surrogate keys.

## GenAI in 15 lines
1. LLM = Transformer that predicts the next token; pre-train → SFT → RLHF/Constitutional AI.
2. Token ≈ 4 chars; context window; cost per input/output token.
3. Self-attention: each token weighs the others (Q, K, V).
4. Temperature 0 for extraction, higher for creative work.
5. Hallucination → RAG + "only from context" + "not found" + citations + validation + human review.
6. Prompt = role + task + delimited data + constraints + format + examples + fallback.
7. Zero/few-shot, chain-of-thought, prompt chaining, system prompt, structured JSON + Pydantic.
8. Prompt injection → treat data as untrusted, least privilege, SELECT-only, human approval.
9. Embedding = meaning vector; cosine similarity; keyword vs semantic → **hybrid**.
10. Vector DB (FAISS, Chroma, pgvector, Qdrant); ANN (HNSW, IVF); metadata filters.
11. RAG: load → clean → chunk (300–800 tokens, overlap) → embed → index → retrieve top-k → rerank → prompt → answer + sources.
12. RAG failures: bad retrieval, lost-in-the-middle, outdated docs, tables → hybrid, rerank, version metadata, table parsing.
13. Evaluation: golden set; Recall@k / MRR; correctness, faithfulness, citation accuracy; LLM-as-judge calibrated against humans; compare versions on the same set; check for regressions.
14. Claude API: `client.messages.create(model, max_tokens, system, messages, temperature, tools)`; stateless (send history); streaming; tool use; prompt caching; Batch API; retries with backoff.
15. RAG vs fine-tuning: prompt first, RAG for knowledge, fine-tune last. Text-to-SQL (Finbot-style) for numbers; **the LLM never computes the reported numbers.**

## Your project – fill this in and memorise it
| Item | My answer |
|---|---|
| Problem / user | |
| Architecture (draw it) | |
| Chunk size / overlap | |
| Embedding model / dims | |
| Vector store / index | |
| k | |
| LLM / temperature | |
| Prompt key rules | |
| Test set size | |
| Accuracy numbers | |
| Hardest bug + fix | |
| Next improvement | |
| GitHub link | |

## Behaviour
- STAR for every story; include a number.
- "I don't know, but here's how I'd find out" beats bluffing.
- Think out loud in coding rounds. State the complexity.
- Ask 2 questions at the end (GenAI use cases in progress; how they evaluate LLM accuracy).
- Confirm you're fine with a 9-month, work-from-office internship in Bengaluru.

## Logistics checklist
- [ ] Resume printed (2 copies) and every line on it rehearsed
- [ ] Laptop charged with the project running locally (in case they ask for a demo)
- [ ] GitHub README polished with an architecture diagram and evaluation table
- [ ] College ID / documents as instructed
- [ ] Reach 15 minutes early (WFO role; first impressions count)
