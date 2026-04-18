import os
import sys

# D: Drive Isolation - Enforce all storage and temp files to D: to avoid C: space exhaustion
BASE_DIR = "D:\\PHEME"
os.environ["TEMP"] = os.path.join(BASE_DIR, "temp")
os.environ["TMP"] = os.path.join(BASE_DIR, "temp")
os.environ["TMPDIR"] = os.path.join(BASE_DIR, "temp")
os.environ["PYTHONPYCACHEPREFIX"] = os.path.join(BASE_DIR, ".pycache")
os.environ["COGNEE_HOME"] = os.path.join(BASE_DIR, ".cognee")
os.environ["SYSTEM_ROOT_DIRECTORY"] = os.path.join(BASE_DIR, ".cognee_system")
os.environ["HF_HOME"] = os.path.join(BASE_DIR, ".huggingface")
os.environ["FAST_EMBED_CACHE"] = os.path.join(BASE_DIR, "temp", "fastembed_cache")
os.environ["SENTENCE_TRANSFORMERS_HOME"] = os.path.join(BASE_DIR, ".huggingface", "sentence_transformers")
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["PYTHONIOENCODING"] = "utf-8"

# Ensure directories exist
for path in [os.environ["TEMP"], os.environ["PYTHONPYCACHEPREFIX"], os.environ["COGNEE_HOME"], os.environ["HF_HOME"]]:
    os.makedirs(path, exist_ok = True)

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App Config
    APP_NAME: str = "PHEME"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    # Neo4j Settings (Updated with user credentials)
    NEO4J_URI: str = "neo4j+s://b2ce99e4.databases.neo4j.io"
    NEO4J_USERNAME: str = "b2ce99e4"
    NEO4J_PASSWORD: str = "Jcf_6zfwnQut4yoeeKu1sRQf7TPwqmnPPlhqOphZUlc"

    # Search API Keys (Placeholders)
    NEWS_API_KEY: str = ""
    GNEWS_API_KEY: str = ""
    GUARDIAN_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    SARVAM_API_KEY: str = ""
    GEMINI_API_KEY: str = ""

    # Qdrant Settings (Updated for Cloud)
    QDRANT_URL: str = "https://b1967e38-cb02-4fc7-927b-bd6fb0fc2dfc.eu-west-1-0.aws.cloud.qdrant.io:6333"
    QDRANT_API_KEY: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwic3ViamVjdCI6ImFwaS1rZXk6NWZmMGM2NGEtZmQxNS00ZWU3LWI4ZjMtMjU4N2VlZDE0MmQyIn0.P0LY_116gxmSEhLAAeri6lhxGvNs7PZh5MPQxf6nbo4"
    # Unified collection name to ensure Cognee creates it with correct dimensions (384 for FastEmbed)
    QDRANT_COLLECTION: str = "pheme_claims_v2" 

    # LLM Settings (Updated for Groq)
    LLM_MODEL: str = "groq/llama-3.3-70b-versatile"
    GROQ_API_KEY: str = "" # Loaded from .env

    # Ollama Settings (Fallback / Local)
    OLLAMA_HOST: str = "http://localhost:11434"

    # Google Cloud Credentials
    GOOGLE_APPLICATION_CREDENTIALS: str = "core/google_creds.json"
    
    # Redis Settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
