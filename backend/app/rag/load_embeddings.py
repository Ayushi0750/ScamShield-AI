import pandas as pd
from sqlalchemy import text

from app.rag.embedding_service import embedding_service
from app.rag.vector_db import vector_engine

BATCH_SIZE = 100

df = pd.read_csv("data/processed/final_data.csv")

total_rows = len(df)

print(f"Total rows: {total_rows}")

# Resume from where the previous run stopped
START_FROM = 1400

for start in range(START_FROM, total_rows, BATCH_SIZE):

    end = min(start + BATCH_SIZE, total_rows)

    batch = df.iloc[start:end]

    with vector_engine.begin() as conn:

        for _, row in batch.iterrows():

            embedding = embedding_service.generate_embedding(
                str(row["text"])
            )

            conn.execute(
                text("""
                    INSERT INTO scam_embeddings
                    (job_text, label, embedding)
                    VALUES
                    (:job_text, :label, :embedding)
                """),
                {
                    "job_text": str(row["text"]),
                    "label": str(row["label"]),
                    "embedding": str(embedding)
                }
            )

    print(f"Processed {end}/{total_rows}")

print("Embedding load completed")