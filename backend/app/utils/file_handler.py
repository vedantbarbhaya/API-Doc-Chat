from pathlib import Path
from typing import Dict, List
import json
from .logger import logger


def load_markdown_files() -> Dict[str, str]:
    """Load all markdown files from knowledge base directory"""
    docs = {}
    kb_dir = Path(__file__).parent.parent / "knowledge_base"

    try:
        for file_path in kb_dir.glob("*.md"):
            with open(file_path, "r", encoding="utf-8") as f:
                docs[file_path.stem] = f.read()
                logger.info(f"Loaded markdown file: {file_path.name}")
        return docs
    except Exception as e:
        logger.error(f"Error loading markdown files: {e}")
        raise


def save_vectorstore(vectorstore, directory: str):
    """Save FAISS index to disk"""
    try:
        vector_store_path = Path(directory)
        vector_store_path.mkdir(parents=True, exist_ok=True)
        vectorstore.save_local(vector_store_path)
        logger.info(f"Saved vector store to {directory}")
    except Exception as e:
        logger.error(f"Error saving vector store: {e}")
        raise


def load_vectorstore(directory: str, embeddings):
    """Load FAISS index from disk"""
    try:
        vector_store_path = Path(directory)
        if vector_store_path.exists():
            from langchain.vectorstores import FAISS
            vectorstore = FAISS.load_local(
                vector_store_path,
                embeddings
            )
            logger.info(f"Loaded vector store from {directory}")
            return vectorstore
        return None
    except Exception as e:
        logger.error(f"Error loading vector store: {e}")
        return None