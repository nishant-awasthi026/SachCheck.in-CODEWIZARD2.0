import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

# Ensure global isolation is set (via core.config)
from core.config import settings

async def test_orchestrator():
    print("--- PHEME AI Orchestrator V2 Verification ---")
    
    from orchestrator.graph import workflow
    
    # Case 1: No Google Fact Check (Triggers 3-Agent Discussion)
    test_claim = {
        "claim_id": "test-v2-001",
        "modality": "text",
        "content": "A new law in India requires all citizens to wear purple on Tuesdays starting next month.",
        "language_hint": "en"
    }
    
    print(f"\n[Case 1] Input Claim: {test_claim['content']}")
    async for output in workflow.astream(test_claim):
        for node_name, state_update in output.items():
            print(f"Node '{node_name}' finished.")

    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    asyncio.run(test_orchestrator())
