"""
retrieval.py
Builds a TF-IDF index over the chunk corpus and retrieves the most
relevant chunks for a given query using cosine similarity.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Retriever:
    def __init__(self, corpus):
        """
        corpus: list of {"category", "filename", "chunk"} dicts from ingestion.build_chunk_corpus
        """
        self.corpus = corpus
        self.texts = [item["chunk"] for item in corpus]
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = self.vectorizer.fit_transform(self.texts)

    def search(self, query, top_k=3):
        """
        Returns the top_k most relevant chunks for the query,
        each with its similarity score and source metadata.
        """
        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.matrix).flatten()
        top_indices = scores.argsort()[::-1][:top_k]

        results = []
        for idx in top_indices:
            if scores[idx] > 0:
                results.append({
                    "chunk": self.corpus[idx]["chunk"],
                    "category": self.corpus[idx]["category"],
                    "filename": self.corpus[idx]["filename"],
                    "score": float(scores[idx])
                })
        return results
