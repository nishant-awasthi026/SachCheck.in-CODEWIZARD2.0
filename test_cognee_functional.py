import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

async def run_functional_test():
    print("--- PHEME Cognee 1.0 (Qdrant Cloud) Functional Test ---")
    
    try:
        from core.graph_rag import graph_rag
        
        test_claim_id = "test-123"
        test_text = "Scientists have discovered a new species of bioluminescent mushrooms in the Amazon rainforest that can purify water."
        
        print(f"Step 1: Ingesting claim into Cognee 1.0: '{test_text}'...")
        await graph_rag.cognify_claim(test_claim_id, test_text)
        print("SUCCESS: Ingestion and Cognification complete.")
        
        print("\nStep 2: Testing Graph-based Retrieval via Cloud Qdrant...")
        results = await graph_rag.search("bioluminescent mushrooms")
        
        print("\n--- Retrieval Results ---")
        print(results)
        print("\nSUCCESS: Test completed successfully!")
        
    except ImportError as e:
        print(f"\nDEPENDENCY ERROR: {e}")
        print("Please ensure you have run: pip install -r requirements.txt")
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_functional_test())
