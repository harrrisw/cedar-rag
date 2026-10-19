"""Inspectable Cedar Lab retrieval. Keyword mode uses only the standard library."""
import argparse
from dataclasses import dataclass
from importlib.metadata import version
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
MODEL = "sentence-transformers/all-MiniLM-L6-v2"
STOPWORDS = set("a an the is are to of in at for and or may can i it be".split())
QUESTIONS = {
    "Q1": "May a trained graduate student operate the laser alone at 19:00?",
    "Q2": "Can I use the laser without another person present?",
    "Q3": "How frequently must I refresh my laser qualification?",
    "Q4": "What is the laser wavelength?",
}
REQUIRED = {"Q1": {"A1", "A2"}, "Q2": {"A2"}, "Q3": {"T1"}, "Q4": set()}


@dataclass(frozen=True)
class Chunk:
    id: str
    filename: str
    text: str


def load_chunks():
    chunks = []
    for path in sorted((ROOT / "docs").glob("*.txt")):
        for paragraph in re.split(r"\n\s*\n", path.read_text(encoding="utf-8").strip()):
            match = re.fullmatch(r"\[([A-Z]\d+)\] (.+)", paragraph)
            if not match:
                raise ValueError(f"Invalid paragraph in {path.name}: {paragraph!r}")
            chunks.append(Chunk(match[1], path.name, match[2]))
    if len(chunks) != 6 or len({c.id for c in chunks}) != 6:
        raise ValueError("Expected exactly six uniquely labeled chunks")
    return sorted(chunks, key=lambda c: c.id)


def words(text):
    return set(re.findall(r"[a-z0-9]+", text.lower())) - STOPWORDS


def keyword_rank(chunks, question):
    query = words(question)
    rows = [(c, len(query & words(c.text)), sorted(query & words(c.text))) for c in chunks]
    return sorted(rows, key=lambda row: (-row[1], row[0].id))


def show_keyword(chunks, question, k=2):
    print(f"Question: {question}\nMethod: keyword; k={k}")
    ranked = keyword_rank(chunks, question)
    for chunk, score, matches in ranked:
        print(f"{chunk.id}: score={score}; matched words={', '.join(matches) or '(none)'}")
    selected = [row for row in ranked if row[1] > 0][:k]
    show_selected(selected)
    return selected


def show_selected(rows):
    if not rows:
        print("No matching passages.")
    else:
        print("Selected: " + ", ".join(row[0].id for row in rows))
        for chunk, *_ in rows:
            print(f"[{chunk.id}] ({chunk.filename}) {chunk.text}")
    print()


class EmbeddingRetriever:
    def __init__(self, chunks):
        import numpy as np
        from sentence_transformers import SentenceTransformer
        self.np, self.chunks = np, chunks
        self.model = SentenceTransformer(MODEL, device="cpu")
        self.documents = self.model.encode_document(
            [c.text for c in chunks], normalize_embeddings=True, convert_to_numpy=True
        )
        if self.documents.shape != (6, 384):
            raise ValueError(f"Unexpected document matrix: {self.documents.shape}")
        if not np.allclose(np.linalg.norm(self.documents, axis=1), 1, atol=1e-6):
            raise ValueError("Document vectors are not normalized")

    def header(self):
        print(f"Model: {MODEL}; device: cpu")
        for package in ("sentence-transformers", "numpy", "torch", "transformers"):
            print(f"{package}=={version(package)}")
        print(f"Document matrix shape: {self.documents.shape}")
        print("All 384 coordinates are used, not just the 12 displayed. Coordinates have no individual semantic labels.")
        for c, v in zip(self.chunks, self.documents):
            print(f"{c.id}: first 12={self.format_vector(v[:12])}; length={self.np.linalg.norm(v):.8f}")
        print()

    @staticmethod
    def format_vector(vector):
        return "[" + ", ".join(f"{x:.4f}" for x in vector) + "]"

    def retrieve(self, question, k=2, inspect=False):
        np = self.np
        query = self.model.encode_query(question, normalize_embeddings=True, convert_to_numpy=True)
        assert query.shape == (384,)
        assert np.isclose(np.linalg.norm(query), 1, atol=1e-6)
        scores = self.documents @ query
        cosine = scores / (np.linalg.norm(self.documents, axis=1) * np.linalg.norm(query))
        assert np.allclose(scores, cosine, atol=1e-6)
        indices = sorted(range(len(self.chunks)), key=lambda i: (-float(scores[i]), self.chunks[i].id))
        ranked = [(self.chunks[i], float(scores[i])) for i in indices]
        print(f"Question: {question}\nMethod: embedding; k={k}")
        print(f"Question vector shape: {query.shape}; first 12={self.format_vector(query[:12])}; length={np.linalg.norm(query):.8f}")
        for chunk, score in ranked:
            print(f"{chunk.id}: score={score:.8f}")
        print("Direct cosine and normalized dot products agree within tolerance (atol=1e-6).")
        if inspect:
            displayed = np.concatenate((self.documents[:, :12].ravel(), query[:12]))
            print(f"Among all displayed document and question coordinates: minimum={displayed.min():.4f}; maximum={displayed.max():.4f}")
            # Float64 arithmetic uses the actual float32 model coordinates without display rounding.
            products = self.documents[indices[0]].astype(np.float64) * query.astype(np.float64)
            print(f"Top passage: {self.chunks[indices[0]].id}")
            print(f"First 12 coordinate products: {self.format_vector(products[:12])}")
            print(f"First 12 subtotal: {products[:12].sum():.8f}")
            print(f"Remaining 372 subtotal: {products[12:].sum():.8f}")
            print(f"Full similarity: {products.sum():.8f}")
            assert np.isclose(products.sum(), scores[indices[0]], atol=1e-6)
        selected = ranked[:k]
        show_selected(selected)
        return selected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("method", choices=["keyword", "embedding"])
    parser.add_argument("question")
    parser.add_argument("-k", type=int, default=2)
    parser.add_argument("--inspect", action="store_true")
    args = parser.parse_args()
    if args.k < 1:
        parser.error("k must be positive")
    chunks = load_chunks()
    if args.method == "keyword":
        show_keyword(chunks, args.question, args.k)
    else:
        retriever = EmbeddingRetriever(chunks)
        retriever.header()
        retriever.retrieve(args.question, args.k, args.inspect)


if __name__ == "__main__":
    main()
