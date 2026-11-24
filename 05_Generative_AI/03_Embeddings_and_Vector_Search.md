# Embeddings & Vector Search (JD: "embeddings, vector search")

### Q1. What is an embedding?
**Answer:** A fixed-length list of numbers (a vector, e.g. 384, 768 or 1024 dimensions) that represents the **meaning** of a piece of text. An embedding model (a Transformer encoder) is trained so that semantically similar texts get nearby vectors.
- **Example 1:** "What is the NPA threshold?" and "After how many overdue days is a loan non-performing?" share few words but have very similar embeddings.
- **Example 2:** Product descriptions "auto loan" and "car finance" sit close together in vector space.

### Q2. Keyword search vs semantic (vector) search?
| Keyword (BM25 / TF-IDF) | Semantic (embeddings) |
|---|---|
| Matches exact words | Matches meaning |
| Great for IDs, codes, names | Great for paraphrases and natural questions |
| Fails on synonyms | Can miss exact codes |
- **Example 1:** Searching "RBI/2024-25/16" → keyword search finds the exact circular. Semantic search may not.
- **Example 2:** Searching "rules for bad loans" → semantic search finds "classification of non-performing assets". Keyword search may not.
- **Best practice:** **Hybrid search** combines both scores (e.g. Reciprocal Rank Fusion).

### Q3. How do you measure similarity between vectors?
**Answer:**
- **Cosine similarity:** the cosine of the angle between vectors (−1 to 1). Ignores length. The most common choice for text.
- **Dot product:** equal to cosine if vectors are normalised.
- **Euclidean (L2) distance:** straight-line distance. Smaller means more similar.
```python
import numpy as np
cos = a @ b / (np.linalg.norm(a) * np.linalg.norm(b))
```
- **Example 1:** cos("loan default", "borrower didn't repay") ≈ 0.8. cos("loan default", "IPL final") ≈ 0.1. (Illustrative values; actual scores depend on the model.)
- **Example 2:** In FAISS, normalise the vectors and use an inner-product index to get cosine similarity.

### Q4. Which embedding models do you know?
**Answer:** Open source: `sentence-transformers` (e.g. `all-MiniLM-L6-v2`, 384 dims, small and fast; `bge`, `e5`, `gte` families). API: OpenAI text-embedding-3, Cohere, Google, **Voyage AI** (Anthropic doesn't offer its own embedding model and recommends Voyage). Check the MTEB leaderboard to compare.
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
vecs = model.encode(["NPA means 90 days overdue", "Car loan interest rate"],
                    normalize_embeddings=True)
print(vecs.shape)   # (2, 384)
```
- **Example 2:** For Indian-language customer complaints, choose a multilingual embedding model.

### Q5. What is a vector database? Examples?
**Answer:** A store optimised for saving vectors with metadata and running fast **nearest-neighbour** search, plus filtering, updates and persistence. Examples: **FAISS** (a library, in-memory), **Chroma** (lightweight, good for prototypes), Pinecone (managed), Weaviate, Qdrant, Milvus, **pgvector** (a Postgres extension), Elasticsearch/OpenSearch (kNN).
- **Example 1:** A prototype RAG app with 5,000 chunks → Chroma or FAISS locally.
- **Example 2:** An enterprise bank that already runs Postgres → pgvector, so data stays in its existing governed database.

### Q6. What is ANN (approximate nearest neighbour)? Why not exact search?
**Answer:** Exact search compares the query with every vector (O(n)), which is slow for millions of vectors. ANN indexes trade a tiny bit of accuracy for big speed-ups. Common ones:
- **HNSW** (graph-based): fast, high recall, more memory.
- **IVF** (clustering): search only the nearest clusters.
- **PQ** (product quantisation): compresses vectors to save memory.
- **Example 1:** 10M chunks → HNSW returns the top 5 in milliseconds.
- **Example 2:** For 5,000 chunks, exact `IndexFlatIP` in FAISS is fine and simpler.

### Q7. Show a minimal FAISS search.
```python
import faiss, numpy as np
from sentence_transformers import SentenceTransformer

docs = ["A loan is NPA if overdue more than 90 days.",
        "LCR must be at least 100 percent.",
        "SMA-2 means 61 to 90 days overdue."]
model = SentenceTransformer("all-MiniLM-L6-v2")
X = model.encode(docs, normalize_embeddings=True).astype("float32")

index = faiss.IndexFlatIP(X.shape[1])   # inner product = cosine (normalised)
index.add(X)

q = model.encode(["When does a loan become non-performing?"], normalize_embeddings=True).astype("float32")
scores, ids = index.search(q, k=2)
for s, i in zip(scores[0], ids[0]):
    print(round(float(s), 3), docs[i])
```
- **Example 2:** The same flow with Chroma: `collection.add(documents=docs, ids=[...], metadatas=[...])`, then `collection.query(query_texts=[q], n_results=2, where={"regulator": "RBI"})`.

### Q8. What is metadata filtering? Why is it important?
**Answer:** You store attributes (source, date, regulator, doc type) with each vector and filter on them before or during search. It improves precision and enforces access control.
- **Example 1:** "What's the latest LCR rule?" → filter `regulator == "APRA"` and sort by date so you don't retrieve an outdated version.
- **Example 2:** A multi-client system filters `client_id == "BankA"` so Bank A never sees Bank B's documents.

### Q9. What is chunking? How do you choose chunk size?
**Answer:** Splitting documents into smaller passages before embedding. If chunks are too big, the embedding gets diluted and you waste context. If they're too small, the chunk loses context. Typical sizes are 200–1000 tokens with 10–20% overlap. Prefer **structure-aware** chunking (by heading, paragraph or section).
- **Example 1:** An RBI master direction is split by numbered paragraph, keeping the heading "Asset Classification" in each chunk's text or metadata.
- **Example 2:** A FAQ document: one chunk per Q&A pair works best.

### Q10. What is re-ranking?
**Answer:** A second stage: retrieve the top ~20–50 candidates cheaply (vector or hybrid search), then re-score them with a more accurate **cross-encoder** reranker (which reads the query and document together) and keep the top 3–5.
- **Example 1:** Vector search returns 20 chunks about "provisioning". The reranker picks the 3 that specifically answer "provisioning for doubtful assets."
- **Example 2:** Cohere Rerank, `bge-reranker` or a cross-encoder from sentence-transformers.

### Q11. How do you evaluate retrieval quality?
**Answer:** Build a set of questions with known relevant chunks. Measure **Recall@k** (is the right chunk in the top k?), **Precision@k**, **MRR** (mean reciprocal rank) and **nDCG**.
- **Example 1:** For 50 questions, the right chunk appears in the top 5 for 44 → Recall@5 = 88%.
- **Example 2:** After switching to hybrid search plus a reranker, Recall@5 rose to 96%.

### Q12. What happens when documents change? How do you update embeddings?
**Answer:** Use upserts keyed by a stable chunk ID, store a document version or hash, re-embed only changed documents, delete superseded chunks or mark them `is_active=False`, and keep `effective_date` metadata. If you change the embedding model, re-embed **everything**, because vectors from different models aren't comparable.
- **Example 1:** RBI amends a circular. Re-embed that circular and mark the old version inactive.
- **Example 2:** Upgrading from MiniLM to bge-large means a full re-index.

### Q13. Can embeddings be used beyond search?
**Answer:** Yes: clustering, classification features, deduplication, anomaly detection, recommendations.
- **Example 1:** Cluster 10,000 complaints to discover new complaint themes.
- **Example 2:** Detect near-duplicate customer records ("Ramesh Kumar, MG Road" vs "Kumar Ramesh, M.G. Rd").
