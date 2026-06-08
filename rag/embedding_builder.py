from sentence_transformers import (SentenceTransformer)
import numpy as np

class EmbeddingBuilder:
    def __init__(self, model_name="BAAI/bge-small-en-v1.5"):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts):
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True
        )

        return embeddings

    def encode_single(self, text):
        return self.model.encode(
            text,
            normalize_embeddings=True
        )

    def save_embeddings(self, embeddings, path):
        np.save(path, embeddings)

    def load_embeddings(self, path):
        return np.load(path)