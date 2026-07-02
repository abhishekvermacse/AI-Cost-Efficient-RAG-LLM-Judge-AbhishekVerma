import os
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

# Base Directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Project Folders
DATA_FOLDER = os.path.join(BASE_DIR, "data")
CHROMA_DB_PATH = os.path.join(BASE_DIR, "chroma_db")
LOG_FOLDER = os.path.join(BASE_DIR, "logs")

# Chunk Settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Embedding Model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Retrieval
TOP_K = 5

# API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")