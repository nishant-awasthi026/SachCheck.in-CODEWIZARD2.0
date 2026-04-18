import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

async def test_orchestrator():
    print("--- PHEME AI Orchestrator Verification ---")
    
    try:
        from orchestrator.graph import workflow
        from core.verifier import verifier
        
        # Mock verifier to avoid network hangs during test
        def mock_verify_parallel(query):
            print(f"--- Mocking verifier for query: {query} ---")
            return {
                "google": [{"claimReview": [{"text": "Fact checked result", "url": "https://example.com"}]}],
                "wikipedia": [{"title": "Wikipedia entry", "snippet": "Snippet"}],
                "ddg": [{"title": "DDG result", "href": "https://duckduckgo.com"}]
            }
        
        verifier.verify_parallel = mock_verify_parallel
        
        # Sample claim for testing
        test_claim = {
            "claim_id": "test-orch-001",
            "modality": "text",
            "content": "The moon is made of green cheese according to recent satellite images from a private mission.",
            "language_hint": "en"
        }
        
        print(f"Input Claim: {test_claim['content']}")
        print("\nStarting orchestrator workflow...")
        
        # Run the workflow
        async for output in workflow.astream(test_claim):
            for node_name, state_update in output.items():
                print(f"\n[Node: {node_name}] completed.")
                # print(f"Update: {state_update}") # Optional: verbose output
        
        print("\n--- Orchestrator Execution Complete ---")
        print("SUCCESS: The orchestrator pipeline finished successfully.")
        
    except Exception as e:
        print(f"\nERROR: ORCHESTRATOR TEST FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_orchestrator())
