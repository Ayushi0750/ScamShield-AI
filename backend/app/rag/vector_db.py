import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

SUPABASE_VECTOR_DB_URL = os.getenv("SUPABASE_VECTOR_DB_URL")

if not SUPABASE_VECTOR_DB_URL:
    raise ValueError("SUPABASE_VECTOR_DB_URL not found in .env")

vector_engine = create_engine(
    SUPABASE_VECTOR_DB_URL,
    echo=False
)