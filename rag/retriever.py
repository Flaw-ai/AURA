import numpy as np
from sklearn.metrics.pairwise import (cosine_similarity)

class Retriever:
    def __init__(self, embeddings, documents):
        self.embeddings = embeddings
        self.documents = documents

    def search(self, query_embedding, top_k=5):
        similarities = cosine_similarity([query_embedding], self.embeddings)[0]
        indices = np.argsort(similarities)[::-1][:top_k]
        results = []

        for idx in indices:
            results.append({
                "score": float(similarities[idx]),
                "document": self.documents[idx]
            })

        return results

    def pretty_print(self, results):
        for i, item in enumerate(results):
            print(f"\n[{i+1}] " f"Score: " f"{item['score']:.4f}")
            print(item["document"]["text"][:300])