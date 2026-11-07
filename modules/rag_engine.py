import fitz
import numpy as np

class SyllabusRAG:
    def __init__(self):
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        except Exception as e:
            raise RuntimeError("Sentence-Transformers could not load. Install optional RAG dependencies and retry.") from e

    def index_pdf(self, uploaded_file):
        doc = fitz.open(stream=uploaded_file.getvalue(), filetype="pdf")
        chunks = []
        for page_no, page in enumerate(doc, start=1):
            text = page.get_text("text").strip()
            words = text.split()
            for i in range(0, len(words), 180):
                part = " ".join(words[i:i+220]).strip()
                if part:
                    chunks.append({"page": page_no, "text": part})
        if not chunks:
            raise ValueError("No selectable text found. This may be a scanned PDF; OCR is not included.")
        vectors = self.model.encode([c["text"] for c in chunks], normalize_embeddings=True)
        for c, v in zip(chunks, vectors):
            c["embedding"] = v
        return chunks

    def retrieve(self, question, chunks, top_k=4):
        q = self.model.encode([question], normalize_embeddings=True)[0]
        scores = [(float(np.dot(q, c["embedding"])), c) for c in chunks]
        scores.sort(key=lambda x: x[0], reverse=True)
        return [dict(page=c["page"], text=c["text"], similarity=s) for s,c in scores[:top_k]]
