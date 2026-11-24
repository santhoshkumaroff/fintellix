# LangChain, LlamaIndex & Vector DBs (JD Good-to-have: "Gen AI Frameworks: LangChain, LlamaIndex, vector databases")

> Framework APIs change fast. Know the **concepts** and be honest about which version you used.

### Q1. What is LangChain?
**Answer:** An open-source framework for building LLM applications by composing building blocks: model wrappers, prompt templates, output parsers, document loaders, text splitters, retrievers, vector store integrations, tools and agents. **LCEL** (LangChain Expression Language) chains components with the `|` operator. **LangGraph** builds stateful, multi-step agent workflows. **LangSmith** handles tracing and evaluation.
- **Example 1:** `prompt | llm | parser` makes a simple chain.
- **Example 2:** A LangGraph agent with nodes: classify question → (SQL tool | RAG tool) → answer → validate.

### Q2. What is LlamaIndex?
**Answer:** A framework focused on **data and retrieval for LLMs**: ingesting documents, building indexes (vector, keyword, tree, knowledge graph), and query engines and chat engines over them. It's strong for RAG out of the box. LlamaParse is its document-parsing service.
- **Example 1:** `VectorStoreIndex.from_documents(docs).as_query_engine().query("What is SMA-2?")`.
- **Example 2:** A sub-question query engine splits "Compare RBI and CBUAE NPA rules" into 2 retrievals.

### Q3. LangChain vs LlamaIndex – when to use which?
| LangChain | LlamaIndex |
|---|---|
| General orchestration, agents, tools, many integrations | RAG-first: ingestion, indexing, retrieval strategies |
| LangGraph for complex agent flows | Rich index types, query engines |
- **Answer line:** "LlamaIndex for retrieval-heavy apps, LangChain/LangGraph for orchestration and agents. They can also be combined. For simple apps, I'd use the plain SDK to keep fewer dependencies."
- **Example 1:** A document Q&A bot → LlamaIndex.
- **Example 2:** A multi-tool assistant (SQL + RAG + email draft) → LangGraph.

### Q4. Show a minimal LangChain RAG chain (conceptual, recent API style).
```python
# pip install langchain langchain-anthropic langchain-community langchain-text-splitters faiss-cpu sentence-transformers pypdf
from langchain_anthropic import ChatAnthropic
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

docs = PyPDFLoader("rbi_npa_circular.pdf").load()
chunks = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100).split_documents(docs)
vs = FAISS.from_documents(chunks, HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"))
retriever = vs.as_retriever(search_kwargs={"k": 4})

prompt = ChatPromptTemplate.from_template(
    "Answer only from the context. If not found, say so.\n<context>{context}</context>\nQuestion: {question}")
llm = ChatAnthropic(model="claude-sonnet-5-5", temperature=0)

def fmt(docs): return "\n\n".join(f"[p{d.metadata.get('page')}] {d.page_content}" for d in docs)

chain = {"context": retriever | fmt, "question": RunnablePassthrough()} | prompt | llm | StrOutputParser()
print(chain.invoke("When is an account classified as NPA?"))
```
- **Example 2:** Swap `FAISS` for `Chroma` with one line change. That's the benefit of the abstraction.

### Q5. What are text splitters? What is `RecursiveCharacterTextSplitter`?
**Answer:** It splits text using a hierarchy of separators (`"\n\n"`, `"\n"`, `" "`, `""`), trying to keep paragraphs, then sentences, together within `chunk_size`, with `chunk_overlap` so context isn't cut at the boundaries.
- **Example 1:** chunk_size=800, overlap=100 for circulars.
- **Example 2:** A markdown or HTML header splitter keeps section titles as metadata.

### Q6. What is an agent in LangChain/LangGraph? Risks?
**Answer:** An LLM that chooses tools in a loop (ReAct: Reason → Act → Observe). Risks: loops, wrong tool calls, cost blow-up, unsafe actions. Mitigations: max iterations, read-only tools, human approval for writes, logging and tracing.
- **Example 1:** Question: "Which branch had the highest NPA growth and why?" Agent: SQL tool → finds the branch → RAG tool → finds commentary documents → answers.
- **Example 2:** Cap it at 5 tool calls. If it isn't solved by then, return a partial answer and escalate.

### Q7. Compare vector databases.
| DB | Type | Use when |
|---|---|---|
| FAISS | Library (Meta), in-memory | Fast prototypes, offline, full control |
| Chroma | Lightweight embedded DB | Local dev, small apps, metadata filters |
| pgvector | Postgres extension | You already use Postgres; want SQL + vectors + governance |
| Qdrant / Weaviate / Milvus | Dedicated vector DBs | Large scale, filtering, hybrid search |
| Pinecone | Fully managed SaaS | No ops, cloud is OK |
| Elasticsearch / OpenSearch | Search engine + kNN | Need strong keyword + vector hybrid |
- **Example 1:** An intern prototype → Chroma persisted to disk.
- **Example 2:** Production in a bank with strict data residency → pgvector or self-hosted Qdrant inside the bank's network.

### Q8. Chroma minimal example?
```python
import chromadb
client = chromadb.PersistentClient(path="./chroma_db")
col = client.get_or_create_collection("circulars")   # default embedding function is used
col.add(ids=["c1", "c2"],
        documents=["NPA: overdue > 90 days", "LCR >= 100%"],
        metadatas=[{"regulator": "RBI"}, {"regulator": "APRA"}])
res = col.query(query_texts=["when is a loan non performing"], n_results=1, where={"regulator": "RBI"})
print(res["documents"])
```

### Q9. Frameworks vs plain SDK – what are the trade-offs?
**Answer:** Frameworks speed up prototyping and integrations, but they add abstraction layers, version churn and harder debugging. For production you often keep only what you need. A good answer: "I prototyped with LangChain, then rewrote the core retrieval and prompt in plain Python plus the Anthropic SDK for transparency and testability."
- **Example 1:** A bug hidden inside a chain's default prompt is hard to find. Plain code makes the prompt explicit.
- **Example 2:** A framework upgrade broke imports (e.g. `langchain.vectorstores` → `langchain_community.vectorstores`). Pin versions.

### Q10. Other tools worth knowing by name
- **Streamlit / Gradio:** quick UIs for demos
- **FastAPI:** serve your RAG as a REST API
- **RAGAS / DeepEval / LangSmith / TruLens:** evaluation and tracing
- **Unstructured / pdfplumber / PyMuPDF / LlamaParse:** document parsing
- **Docker:** package the app
- **Example:** "My project: FastAPI backend + Streamlit UI + Chroma + Claude, evaluated with a 40-question golden set."
