import os

# Environment variables MUST be set before importing cognee to avoid connection test failures
os.environ["ENABLE_BACKEND_ACCESS_CONTROL"] = "false"
os.environ["COGNEE_SKIP_CONNECTION_TEST"] = "true"
os.environ["HUGGINGFACE_TOKENIZER"] = "Salesforce/SFR-Embedding-Mistral"

# Ensure all Cognee data is on D: drive
BASE_DIR = "d:/PHEME"
os.environ["COGNEE_HOME"] = os.path.join(BASE_DIR, ".cognee")
os.environ["SYSTEM_ROOT_DIRECTORY"] = os.path.join(BASE_DIR, ".cognee_system")
os.environ["COGNEE_SYSTEM_DIRECTORY"] = os.path.join(BASE_DIR, ".cognee_system")

# Attempt to import Cognee, with fallback for memory-constrained environments
try:
    import cognee
    from cognee import config
    from cognee.infrastructure.databases.vector import use_vector_adapter
    COGNEE_LOADED = True
except (ImportError, MemoryError) as e:
    print(f"Warning: Cognee could not be loaded ({type(e).__name__}). Using fallback GraphRAG.")
    COGNEE_LOADED = False
from core.config import settings

# Fix for QDrantAdapter signature mismatches in Cognee 1.0
try:
    from cognee_community_vector_adapter_qdrant import QDrantAdapter
    
    class FixedQDrantAdapter(QDrantAdapter):
        def __init__(self, url, api_key, embedding_engine, qdrant_path = None, database_name = None, **kwargs):
            # Cognee 1.0 passes more arguments than the community adapter's __init__ might expect
            super().__init__(url = url, api_key = api_key, embedding_engine = embedding_engine, qdrant_path = qdrant_path)

        async def search(self, collection_name: str, query: str = None, query_vector: list[float] = None, limit: int = 5, **kwargs):
            # Cognee 1.0 passes 'query', but the community adapter expects 'query_text'
            return await super().search(
                collection_name = collection_name,
                query_text = query,
                query_vector = query_vector,
                limit = limit
            )

    use_vector_adapter("qdrant", FixedQDrantAdapter)
except ImportError:
    print("Warning: cognee-community-vector-adapter-qdrant not found.")

# Ensure Cognee directories exist
kuzu_dir = os.path.abspath(".cognee/databases/kuzu_db")
system_root = os.environ.get("SYSTEM_ROOT_DIRECTORY")
db_folder = os.path.join(system_root, "databases") if system_root else None

for d in [os.path.dirname(kuzu_dir), system_root, db_folder]:
    if d:
        try:
            if os.path.exists(d) and not os.path.isdir(d):
                os.remove(d) # Remove if it's a file collision
            os.makedirs(d, exist_ok = True)
        except Exception as e:
            print(f"Warning: Could not create directory {d}: {e}")

if COGNEE_LOADED and system_root:
    config.system_root_directory(system_root)

# Cognee 1.0 Configuration
if COGNEE_LOADED:
    # Vector DB (Qdrant Cloud)
    config.set_vector_db_config({
        "vector_db_provider": "qdrant",
        "vector_db_url": settings.QDRANT_URL,
        "vector_db_key": settings.QDRANT_API_KEY,
    })
    
    # Graph DB (Neo4j)
    config.set_graph_db_config({
        "graph_database_provider": "neo4j",
        "graph_database_url": settings.NEO4J_URI,
        "graph_database_username": settings.NEO4J_USERNAME,
        "graph_database_password": settings.NEO4J_PASSWORD,
    })
    
    # LLM Config (Using Groq)
    config.set_llm_config({
        "llm_provider": "custom",
        "llm_model": settings.LLM_MODEL,
        "llm_endpoint": "https://api.groq.com/openai/v1",
        "llm_api_key": settings.GROQ_API_KEY or os.getenv("GROQ_API_KEY"), 
    })
    
    # Embedding Config (FastEmbed for local performance)
    config.set_embedding_config({
        "embedding_provider": "fastembed",
        "embedding_model": "BAAI/bge-small-en-v1.5",
        "embedding_dimensions": 384,
    })

class GraphRAG:
    def __init__(self):
        self.initialized = False

    async def _ensure_initialized(self):
        # Placeholder for any async init if needed by future Cognee versions
        self.initialized = True

    async def cognify_claim(self, claim_id: str, claim_text: str, verdict: str = None, explanation: str = None, counter_narrative: str = None):
        """Ingest text into the graph and vector store."""
        if not COGNEE_LOADED:
            return
            
        # Combine the result into a comprehensive verification record for Cognee
        record = f"CLAIM: {claim_text}\n"
        if verdict: record += f"VERDICT: {verdict}\n"
        if explanation: record += f"EXPLANATION: {explanation}\n"
        if counter_narrative: record += f"COUNTER_NARRATIVE: {counter_narrative}\n"
        
        try:
            await cognee.add(record, dataset_name = f"claim_{claim_id}")
            await cognee.cognify()
        except Exception as e:
            print(f"Warning: Insight could not be persisted to graph ({e})")

    async def search(self, query: str):
        """Search the graph-based RAG."""
        if not COGNEE_LOADED:
            return "Graph search unavailable due to memory constraints."
        try:
            results = await cognee.search(query)
            return results
        except Exception as e:
            # Handle SearchPreconditionError (422) if graph is empty/uninitialized
            print(f"Warning: Graph search skipped ({e})")
            return "No historical graph evidence found."

graph_rag = GraphRAG()
