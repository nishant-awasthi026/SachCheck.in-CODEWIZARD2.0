from qdrant_client import QdrantClient
from qdrant_client.http import models
from core.config import settings

class VectorStore:
    def __init__(self):
        # We use in-memory for testing if docker is unavailable, otherwise connect to docker
        try:
            self.client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)
            # Try getting collections to test connection
            self.client.get_collections()
        except Exception:
            print("Warning: Could not connect to Qdrant server, falling back to in-memory mode")
            self.client = QdrantClient(":memory:")

        self._ensure_collection()

    def _ensure_collection(self):
        collections = [c.name for c in self.client.get_collections().collections]
        if settings.QDRANT_COLLECTION not in collections:
            self.client.create_collection(
                collection_name=settings.QDRANT_COLLECTION,
                vectors_config=models.VectorParams(
                    size=1536,  # Size for typical embeddings, adjust based on model used
                    distance=models.Distance.COSINE
                )
            )

    def upsert(self, id: str, vector: list, payload: dict):
        self.client.upsert(
            collection_name=settings.QDRANT_COLLECTION,
            points=[
                models.PointStruct(
                    id=id,
                    vector=vector,
                    payload=payload
                )
            ]
        )

    def search(self, vector: list, limit: int = 5):
        return self.client.search(
            collection_name=settings.QDRANT_COLLECTION,
            query_vector=vector,
            limit=limit
        )

qdrant_store = VectorStore()
