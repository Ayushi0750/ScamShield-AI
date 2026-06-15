import pandas as pd
from sqlalchemy import text

from app.rag.embedding_service import embedding_service
from app.rag.vector_db import vector_engine

# Load first 10 rows
df = pd.read_csv("data/processed/final_data.csv").head(10)

with vector_engine.begin() as conn:
    for _, row in df.iterrows():

        embedding = embedding_service.generate_embedding(row["text"])

        conn.execute(
            text("""
                INSERT INTO scam_embeddings
                (job_text, label, embedding)
                VALUES
                (:job_text, :label, :embedding)
            """),
            {
                "job_text": row["text"],
                "label": str(row["label"]),
                "embedding": str(embedding)
            }
        )

print("Inserted 10 records successfully")