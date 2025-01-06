# backend/app/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"
VECTOR_STORE_DIR = BASE_DIR / "vector_store" / "faiss_index"

# Create directories if they don't exist
KNOWLEDGE_BASE_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

# OpenAI API settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Model settings
MODEL_SETTINGS = {
    "embedding_model": "text-embedding-ada-002",
    "chat_model": "gpt-4o-mini",
    "temperature": 0.7,
    "max_tokens": 1000
}

# Vector store settings
VECTOR_STORE_SETTINGS = {
    "chunk_size": 1000,
    "chunk_overlap": 200,
    "k_retrieval": 3
}

# API settings
CORS_ORIGINS = [
    "http://localhost:5173",  # Vite default
    "http://localhost:3000"   # Alternative frontend port
]