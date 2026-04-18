from neo4j import GraphDatabase
from qdrant_client import QdrantClient
from core.config import settings

def cleanup_data():
    print("Starting data cleanup...")
    
    # 1. Clear Neo4j
    try:
        driver = GraphDatabase.driver(
            settings.NEO4J_URI, 
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )
        with driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
        driver.close()
        print("Neo4j data cleared.")
    except Exception as e:
        print(f"Neo4j cleanup failed: {e}")

    # 2. Clear Qdrant
    try:
        client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)
        # Instead of deleting the whole engine, we just delete the specific collection
        client.delete_collection(collection_name=settings.QDRANT_COLLECTION)
        print(f"Qdrant collection '{settings.QDRANT_COLLECTION}' cleared.")
    except Exception as e:
        print(f"Qdrant cleanup failed: {e}")

if __name__ == "__main__":
    cleanup_data()
