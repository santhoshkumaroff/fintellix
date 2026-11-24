"""
RegDoc Q&A - a small RAG pipeline over regulatory documents.

Pipeline:  load docs -> chunk -> embed -> index -> retrieve top-k -> prompt Claude -> answer + sources

Embeddings:
  - default: sentence-transformers "all-MiniLM-L6-v2" + FAISS (pip install sentence-transformers faiss-cpu)
  - fallback: TF-IDF (scikit-learn) so the retrieval part runs even without those libraries.
LLM:
  - Anthropic Claude (pip install anthropic, set ANTHROPIC_API_KEY). Use --no-llm to see retrieval only.
"""
from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np

MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5")   # check docs for current model IDs

SYSTEM_RULES = """You answer questions about banking regulations.
Use ONLY the text inside <context>. Each chunk starts with an id like [c3].
If the context does not contain the answer, reply exactly:
"I could not find this in the provided documents."
Quote numbers exactly as written. Do not use outside knowledge.
End with a line: Sources: [ids you used]"""


# ---------- 1. Load ----------
def load_documents(folder: str) -> list[dict]:
    docs = []
    for path in sorted(Path(folder).iterdir()):
        if path.suffix.lower() == ".txt" or path.suffix.lower() == ".md":
            docs.append({"source": path.name, "text": path.read_text(encoding="utf-8")})
        elif path.suffix.lower() == ".pdf":
            from pypdf import PdfReader
            pages = [p.extract_text() or "" for p in PdfReader(str(path)).pages]
            docs.append({"source": path.name, "text": "\n".join(pages)})
    return docs


# ---------- 2. Chunk ----------
@dataclass
class Chunk:
    id: str
    source: str
    text: str


def chunk_document(doc: dict, max_words: int = 120, overlap_words: int = 20) -> list[str]:
    """Paragraph-aware chunking: keep paragraphs together, split only very long ones."""
    paras = [p.strip() for p in re.split(r"\n\s*\n", doc["text"]) if p.strip()]
    chunks, current = [], []
    for para in paras:
        words = para.split()
        if len(current) + len(words) > max_words and current:
            chunks.append(" ".join(current))
            current = current[-overlap_words:]          # overlap keeps context across boundaries
        current.extend(words)
    if current:
        chunks.append(" ".join(current))
    return chunks


def build_chunks(docs: list[dict]) -> list[Chunk]:
    out, n = [], 0
    for d in docs:
        for text in chunk_document(d):
            n += 1
            out.append(Chunk(id=f"c{n}", source=d["source"], text=text))
    return out


# ---------- 3. Embed + index ----------
class Retriever:
    def __init__(self, chunks: list[Chunk]):
        self.chunks = chunks
        texts = [c.text for c in chunks]
        try:
            from sentence_transformers import SentenceTransformer
            import faiss
            self.kind = "minilm+faiss"
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            X = self.model.encode(texts, normalize_embeddings=True).astype("float32")
            self.index = faiss.IndexFlatIP(X.shape[1])     # inner product on normalised vectors = cosine
            self.index.add(X)
        except ImportError:
            from sklearn.feature_extraction.text import TfidfVectorizer
            self.kind = "tfidf"
            self.vec = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
            self.X = self.vec.fit_transform(texts)

    def search(self, query: str, k: int = 4) -> list[tuple[float, Chunk]]:
        if self.kind == "minilm+faiss":
            q = self.model.encode([query], normalize_embeddings=True).astype("float32")
            scores, ids = self.index.search(q, k)
            return [(float(s), self.chunks[i]) for s, i in zip(scores[0], ids[0]) if i != -1]
        q = self.vec.transform([query])
        scores = (self.X @ q.T).toarray().ravel()           # TF-IDF rows are L2-normalised -> cosine
        top = np.argsort(scores)[::-1][:k]
        return [(float(scores[i]), self.chunks[i]) for i in top]


# ---------- 4. Generate ----------
def build_prompt(question: str, hits: list[tuple[float, Chunk]]) -> str:
    context = "\n\n".join(f"[{c.id}] ({c.source}) {c.text}" for _, c in hits)
    return f"<context>\n{context}\n</context>\n\nQuestion: {question}"


def ask_claude(prompt: str) -> str:
    from anthropic import Anthropic
    client = Anthropic()                                     # reads ANTHROPIC_API_KEY
    msg = client.messages.create(
        model=MODEL, max_tokens=500, temperature=0,
        system=SYSTEM_RULES,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


def answer(retriever: Retriever, question: str, k: int = 4, use_llm: bool = True) -> dict:
    hits = retriever.search(question, k)
    prompt = build_prompt(question, hits)
    text = ask_claude(prompt) if use_llm else "(LLM skipped)"
    return {"question": question, "answer": text,
            "retrieved": [{"id": c.id, "source": c.source, "score": round(s, 3)} for s, c in hits]}


# ---------- 5. Evaluate retrieval ----------
def evaluate_retrieval(retriever: Retriever, golden_path: str, k: int = 4) -> float:
    golden = json.loads(Path(golden_path).read_text())
    hits_total = 0
    for case in golden:
        texts = " ".join(c.text.lower() for _, c in retriever.search(case["question"], k))
        found = all(kw.lower() in texts for kw in case["must_contain"])
        hits_total += found
        print(f"{'PASS' if found else 'FAIL'}  {case['question']}")
    recall = hits_total / len(golden)
    print(f"\nRecall@{k} (keyword-based): {recall:.0%}  on {len(golden)} questions  [{retriever.kind}]")
    return recall


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", default="docs")
    ap.add_argument("--ask")
    ap.add_argument("--eval", action="store_true")
    ap.add_argument("--no-llm", action="store_true")
    ap.add_argument("-k", type=int, default=4)
    args = ap.parse_args()

    chunks = build_chunks(load_documents(args.docs))
    retriever = Retriever(chunks)
    print(f"Indexed {len(chunks)} chunks using {retriever.kind}")

    if args.eval:
        evaluate_retrieval(retriever, "eval/golden_set.json", args.k)
    if args.ask:
        print(json.dumps(answer(retriever, args.ask, args.k, use_llm=not args.no_llm), indent=2))
