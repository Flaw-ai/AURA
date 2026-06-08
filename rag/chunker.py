from typing import List
import re

try:
    from sentence_transformers import (SentenceTransformer)
    from sklearn.metrics.pairwise import (cosine_similarity)
    SEMANTIC_AVAILABLE = True

except Exception:
    SEMANTIC_AVAILABLE = False


class Chunker:
    def __init__(self, chunk_size=200, overlap=50):
        self.chunk_size = chunk_size
        self.overlap = overlap

        if SEMANTIC_AVAILABLE:
            self.embedding_model = (SentenceTransformer("BAAI/bge-small-en-v1.5"))
            
    def sentence_split(self, text: str) -> List[str]:
        sentences = re.split(
            r'(?<=[.!?])\s+',
            text
        )

        return [
            s.strip()
            for s in sentences
            if s.strip()
        ]

    def chunk_text(self, text: str) -> List[str]:
        words = text.split()
        chunks = []
        start = 0

        while start < len(words):
            end = start + self.chunk_size
            chunk = words[start:end]
            chunks.append(" ".join(chunk))
            start += (self.chunk_size - self.overlap)

        return chunks

    def sentence_chunking(self, text: str, max_sentences=8):
        sentences = self.sentence_split(text)
        chunks = []
        for i in range(
            0,
            len(sentences),
            max_sentences
        ):
            chunk = (sentences[i: i + max_sentences])
            chunks.append(" ".join(chunk))

        return chunks

    def recursive_chunking(self, text: str):
        paragraphs = text.split("\n\n")
        final_chunks = []
        for paragraph in paragraphs:
            word_count = len(paragraph.split())
            
            if (word_count <= self.chunk_size):
                final_chunks.append(paragraph)

            else:
                final_chunks.extend(self.chunk_text(paragraph))

        return final_chunks

    def semantic_chunking(
        self, text: str, threshold=0.75):

        if not SEMANTIC_AVAILABLE:
            return self.sentence_chunking(
                text
            )

        sentences = self.sentence_split(text)

        if len(sentences) < 2:
            return [text]

        embeddings = (
            self.embedding_model.encode(
                sentences,
                normalize_embeddings=True
            )
        )

        chunks = []

        current_chunk = [
            sentences[0]
        ]

        for i in range(
            1,
            len(sentences)
        ):

            similarity = (
                cosine_similarity(
                    [embeddings[i - 1]],
                    [embeddings[i]]
                )[0][0]
            )

            if similarity >= threshold:
                current_chunk.append(sentences[i])

            else:
                chunks.append(
                    " ".join(current_chunk))
                current_chunk = [sentences[i]]

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def chunk_document(self, document, strategy="semantic"):
        text = document["text"]
        if strategy == "fixed":
            chunks = (self.chunk_text(text))

        elif strategy == "sentence":
            chunks = (self.sentence_chunking(text))

        elif strategy == "recursive":
            chunks = (self.recursive_chunking(text))

        else:
            chunks = (self.semantic_chunking(text))

        results = []

        for idx, chunk in enumerate(chunks):
            results.append(
                {
                    "chunk_id": idx,
                    "source":
                    document.get(
                        "source",
                        "unknown"
                    ),
                    "text": chunk
                }
            )

        return results

    def statistics(self, chunks):
        lengths = [
            len(c["text"].split())
            if isinstance(
                c,
                dict
            )
            else len(
                c.split()
            )
            for c in chunks
        ]

        return {
            "chunks": len(chunks),
            "avg_words": sum(lengths) / max(len(lengths), 1),
            "max_words": max(lengths, default=0),
            "min_words":min(lengths, default=0)
        }