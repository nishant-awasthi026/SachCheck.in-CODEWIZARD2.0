import asyncio
import cognee
import os
from cognee import config

async def test():
    # Minimized config
    config.set_graph_db_config({
        "graph_database_provider": "kuzu",
        "graph_file_path": os.path.abspath("test_cognee_kuzu"),
    })
    
    # Use standard LLM/Embedding defaults if possible, or dummy
    config.set_llm_config({
        "llm_provider": "openai",
        "llm_api_key": "dummy"
    })
    
    try:
        print("Adding data...")
        await cognee.add("Test data", dataset_name="test")
        print("Cognifying...")
        await cognee.cognify()
        print("Search...")
        results = await cognee.search("Test")
        print(results)
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test())
