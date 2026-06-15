from sqlalchemy import text
from app.database.session import SessionLocal
from sentence_transformers import SentenceTransformer
import torch

# Lazy-loaded model
_model = None


def get_model():
    global _model

    if _model is None:
        print("Loading embedding model...")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        print("Embedding model loaded.")

    return _model


class ScamRetriever:

    def __init__(self):
        self.db = SessionLocal()

    def get_embedding(self, text_input: str):
        """
        Convert input text into embedding vector
        """

        model = get_model()

        with torch.no_grad():
            embedding = model.encode(
                text_input,
                convert_to_numpy=True,
                normalize_embeddings=True,
                show_progress_bar=False
            )

        return embedding.tolist()

    def search_similar_cases(self, query: str, top_k: int = 5):
        """
        Fetch top-K similar scam cases from pgvector
        """

        query_embedding = self.get_embedding(query)

        vector_string = "[" + ",".join(map(str, query_embedding)) + "]"

        sql = text("""
            SELECT
                id,
                job_text,
                label,
                1 - (embedding <=> CAST(:query_embedding AS vector)) AS similarity
            FROM scam_embeddings
            ORDER BY embedding <=> CAST(:query_embedding AS vector)
            LIMIT :top_k
        """)

        result = self.db.execute(
            sql,
            {
                "query_embedding": vector_string,
                "top_k": top_k
            }
        ).fetchall()

        return [
            {
                "id": row.id,
                "text": row.job_text,
                "label": row.label,
                "similarity": round(float(row.similarity), 4)
            }
            for row in result
        ]


# Singleton instance
retriever = ScamRetriever()