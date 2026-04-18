from neo4j import GraphDatabase
from core.config import settings

class GraphStore:
    def __init__(self):
        self.driver = None
        self._connect()

    def _connect(self):
        try:
            self.driver = GraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
            )
            # Verify connection
            self.driver.verify_connectivity()
        except Exception as e:
            print(f"Warning: Could not connect to Neo4j at {settings.NEO4J_URI}. Exception: {e}")
            self.driver = None

    def close(self):
        if self.driver:
            self.driver.close()

    def add_triplet(self, subject: str, predicate: str, obj: str):
        if not self.driver:
            return
        
        query = (
            "MERGE (s:Entity {name: $subject}) "
            "MERGE (o:Entity {name: $obj}) "
            "MERGE (s)-[r:RELATION {type: $predicate}]->(o)"
        )
        with self.driver.session() as session:
            session.run(query, subject=subject, predicate=predicate, obj=obj)

    def get_related_entities(self, entity: str):
        if not self.driver:
            return []
        
        query = (
            "MATCH (e:Entity {name: $entity})-[r:RELATION]-(related) "
            "RETURN e.name as entity, r.type as relation, related.name as related_entity"
        )
        with self.driver.session() as session:
            result = session.run(query, entity=entity)
            return [record.data() for record in result]

neo4j_store = GraphStore()
