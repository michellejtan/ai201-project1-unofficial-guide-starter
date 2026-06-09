"""Central configuration — single source of truth for models, paths, and retrieval settings.
Imported by ingest.py (Milestone 3), retrieve.py (Milestone 4), and app.py (Milestone 5)."""

import os

from dotenv import load_dotenv

load_dotenv()  # read GROQ_API_KEY from .env

# --- LLM (Milestone 5) ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = "llama-3.3-70b-versatile"

# --- Embeddings (Milestone 4) ---
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# --- Vector store (Milestone 4) ---
CHROMA_COLLECTION = "ccsf_cs_reviews"
CHROMA_PATH = os.path.join(os.path.dirname(__file__), "chroma_db")

# --- Retrieval (Milestone 4) ---
N_RESULTS = 5  # top-k; matches planning.md Retrieval Approach

# --- Documents (Milestone 3) ---
DOCS_PATH = os.path.join(os.path.dirname(__file__), "documents")
