"""
Application Configuration

All project settings are centralized here.
"""

# ==========================================================
# Application
# ==========================================================

APP_NAME = "Agentic Research Assistant"
VERSION = "2.0.0"

# ==========================================================
# Search
# ==========================================================

# Number of search results to fetch
MAX_RESULTS = 5

# ==========================================================
# Retrieval
# ==========================================================

# Number of retrieved chunks
TOP_K = 10

# ==========================================================
# Chunking
# ==========================================================

# Maximum characters per chunk
CHUNK_SIZE = 500

# Characters shared between chunks
CHUNK_OVERLAP = 100

# ==========================================================
# Models
# ==========================================================

# Embedding model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Cross Encoder reranker
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L6-v2"

# ==========================================================
# Cache
# ==========================================================

CACHE_ENABLED = True

# SQLite database
CACHE_DB = "storage/cache.db"

# Cache expiry (seconds)
CACHE_EXPIRY = 60 * 60 * 24  # 24 Hours

# ==========================================================
# Vector Database
# ==========================================================

FAISS_INDEX_PATH = "storage/faiss.index"
FAISS_METADATA_PATH = "storage/metadata.pkl"

# ==========================================================
# Networking
# ==========================================================

REQUEST_TIMEOUT = 20

MAX_CONCURRENT_REQUESTS = 10

MAX_RETRIES = 3

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 "
    "(KHTML, like Gecko) "
    "Chrome/138.0 Safari/537.36"
)

# ==========================================================
# Summarization
# ==========================================================

MAX_SUMMARY_SENTENCES = 12

# ==========================================================
# Logging
# ==========================================================

LOG_LEVEL = "INFO"

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(message)s"
)

# ==========================================================
# Session Memory
# ==========================================================

MAX_HISTORY = 10

# ==========================================================
# Report
# ==========================================================

REPORT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# ==========================================================
# Storage
# ==========================================================

STORAGE_DIR = "storage"

# ==========================================================
# API
# ==========================================================

API_PREFIX = "/"

# ==========================================================
# Feature Flags
# ==========================================================

ENABLE_CACHE = True
ENABLE_RERANKING = True
ENABLE_REPORT = True
ENABLE_MARKDOWN = True
ENABLE_SESSION_MEMORY = True
ENABLE_DUPLICATE_REMOVAL = True