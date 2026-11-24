# Rapid-Fire 100 – one-line answers (cover the answer column and quiz yourself)

| # | Question | One-line answer |
|---|---|---|
| 1 | Parent company of Fintellix? | ICRA Ltd (Moody's is its largest shareholder) |
| 2 | Fintellix HQ? | Bengaluru |
| 3 | What is Finbot? | Fintellix's conversational AI giving data insights via SQL queries |
| 4 | RegTech vs SupTech? | Tools for regulated firms vs tools for regulators |
| 5 | NPA threshold? | Overdue > 90 days |
| 6 | SMA-1 range? | 31–60 days overdue |
| 7 | ECL formula? | PD × LGD × EAD |
| 8 | ECL Stage 2? | Significant increase in credit risk → lifetime ECL |
| 9 | LCR minimum? | 100% |
| 10 | BCBS 239 about? | Risk data aggregation & reporting principles |
| 11 | RBI's new data warehouse? | CIMS |
| 12 | XBRL? | XML-based tagged business-reporting standard |
| 13 | Maker-checker? | One prepares, a different person approves |
| 14 | Data lineage? | Trace a reported number back to source rows and rules |
| 15 | GNPA vs NNPA? | NNPA = GNPA − provisions |
| 16 | list vs tuple? | Mutable vs immutable (tuple hashable) |
| 17 | Why a set for membership? | O(1) average lookup |
| 18 | dict internals? | Hash table |
| 19 | `is` vs `==`? | Identity vs value |
| 20 | Shallow vs deep copy? | Shared inner objects vs fully independent |
| 21 | Generator? | Lazy values via `yield`; memory-efficient |
| 22 | Decorator? | Function wrapping a function to add behaviour |
| 23 | `*args`, `**kwargs`? | Extra positional (tuple), extra keyword (dict) |
| 24 | Mutable default fix? | Default `None`, create inside |
| 25 | LEGB? | Local, Enclosing, Global, Built-in |
| 26 | 4 OOP pillars? | Encapsulation, abstraction, inheritance, polymorphism |
| 27 | `self`? | Reference to the current instance |
| 28 | classmethod use? | Alternative constructors (`from_dict`) |
| 29 | ABC? | Abstract base class forcing method implementation |
| 30 | Why `with`? | Guaranteed cleanup (context manager) |
| 31 | Bare `except` problem? | Hides bugs; catch specific exceptions |
| 32 | GIL impact? | Threads for I/O; processes for CPU |
| 33 | 0.1+0.2==0.3? | False; use Decimal for money |
| 34 | `if __name__ == "__main__"`? | Runs only when executed directly |
| 35 | venv why? | Isolated dependencies per project |
| 36 | Secrets storage? | Env vars / .env (gitignored) / secrets manager |
| 37 | NumPy faster why? | Contiguous typed arrays, vectorised C ops |
| 38 | Broadcasting? | Auto-expanding shapes for element-wise ops |
| 39 | axis=0? | Down the rows → one result per column |
| 40 | loc vs iloc? | Label vs position |
| 41 | Filter with 2 conditions? | `(a) & (b)` with parentheses |
| 42 | Find recon breaks in pandas? | Outer merge with `indicator=True` |
| 43 | groupby named agg? | `.agg(total=("col","sum"))` |
| 44 | apply vs vectorised? | Vectorised is much faster |
| 45 | Big CSV? | `chunksize`, `usecols`, dtypes, DuckDB/Polars |
| 46 | Missing values in regulatory data? | Flag & report; don't silently fill |
| 47 | Outlier rule? | IQR (1.5×) or z-score > 3; flag, don't delete |
| 48 | WHERE vs HAVING? | Before vs after grouping |
| 49 | LEFT JOIN anti-join? | `LEFT JOIN ... WHERE right.key IS NULL` |
| 50 | RANK vs DENSE_RANK? | 1,1,3 vs 1,1,2 |
| 51 | NOT IN trap? | A NULL in the subquery → no rows; use NOT EXISTS |
| 52 | CTE? | Named temporary result (`WITH`) |
| 53 | SQL injection fix? | Parameterised queries, least privilege |
| 54 | ACID? | Atomicity, Consistency, Isolation, Durability |
| 55 | OLTP vs OLAP? | Transactions vs analytics |
| 56 | ETL vs ELT? | Transform before vs after loading |
| 57 | Fact vs dimension? | Measures vs descriptive context |
| 58 | Star vs snowflake? | Denormalised vs normalised dimensions |
| 59 | SCD Type 2? | New row with validity dates (history) |
| 60 | Grain? | What one fact row represents |
| 61 | git fetch vs pull? | Download only vs download + merge |
| 62 | Merge vs rebase? | Merge commit vs linear replay (don't rebase shared branches) |
| 63 | Undo a pushed commit? | `git revert` |
| 64 | .gitignore for? | Secrets, venv, data, caches |
| 65 | `2>&1`? | Redirect stderr to stdout |
| 66 | chmod 755? | rwx owner, r-x group, r-x others |
| 67 | Cron for? | Scheduling jobs |
| 68 | LLM? | Transformer trained to predict the next token on huge text |
| 69 | Token? | ~4 chars of text; unit of cost and limits |
| 70 | Context window? | Max tokens the model sees at once |
| 71 | Self-attention? | Each token weighs every other token's relevance |
| 72 | Temperature? | Randomness; 0 = focused |
| 73 | Hallucination? | Fluent but false output |
| 74 | Reduce hallucination? | RAG, strict prompt, citations, validation, human review |
| 75 | Zero vs few-shot? | No examples vs a few examples in the prompt |
| 76 | Chain-of-thought? | Step-by-step reasoning before the answer |
| 77 | System prompt? | Persistent rules/role for the conversation |
| 78 | Structured output? | Schema + JSON + Pydantic validation + retry |
| 79 | Prompt injection? | Malicious text overriding instructions |
| 80 | Embedding? | Vector representing meaning |
| 81 | Cosine similarity? | Angle-based similarity of vectors |
| 82 | Hybrid search? | Keyword (BM25) + semantic combined |
| 83 | Vector DBs? | FAISS, Chroma, pgvector, Qdrant, Pinecone |
| 84 | HNSW? | Graph-based ANN index |
| 85 | Chunking? | Split docs into ~300–800 token passages with overlap |
| 86 | Reranker? | Cross-encoder re-scoring top candidates |
| 87 | RAG in one line? | Retrieve relevant docs → add to prompt → generate grounded answer |
| 88 | Lost in the middle? | Middle-of-context info gets used less |
| 89 | RAG vs fine-tune? | Knowledge vs behaviour/format |
| 90 | Recall@k? | % of questions with the right chunk in the top k |
| 91 | Faithfulness? | Answer supported by the retrieved context |
| 92 | LLM-as-judge? | An LLM grades outputs against a rubric |
| 93 | Compare 2 prompt versions? | Same golden set, metrics side by side, check regressions |
| 94 | Claude API call? | `client.messages.create(model, max_tokens, messages, system)` |
| 95 | API is stateless means? | Send the conversation history every call |
| 96 | Tool use? | Model requests a function; your code runs it and returns the result |
| 97 | Cut LLM cost? | Smaller model, RAG, prompt caching, Batch API, cap tokens |
| 98 | MCP? | Open protocol connecting AI apps to tools/data |
| 99 | Text-to-SQL safety? | Read-only user, SELECT-only, table allow-list, show the SQL |
| 100 | Golden rule for GenAI in reporting? | The LLM assists; code/SQL computes the numbers; a human approves |
