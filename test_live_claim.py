import asyncio
import sys
import os
import json

# Add project root to path
sys.path.append(os.getcwd())

async def test_specific_claim():
    from orchestrator.graph import workflow
    
    claim_text = "BJP's Samrat Choudhary Becomes First Chief Minister in Bihar"
    test_input = {
        "claim_id": "live-test-001",
        "modality": "text",
        "content": claim_text,
        "language_hint": "en"
    }
    
    print(f"--- PHEME Live Test: '{claim_text}' ---")
    
    # Run the orchestrator
    final_state = await workflow.ainvoke(test_input)
    
    print("\n" + "="*50)
    print("FINAL ORCHESTRATOR DECISION")
    print("="*50)
    print(f"VERDICT: {final_state.get('final_verdict')}")
    print(f"EXPLANATION: {final_state.get('explanation')}")
    print(f"COUNTER-NARRATIVE: {final_state.get('counter_narrative')}")
    
    links = final_state.get("links", [])
    if links:
        print("\nREFERENCES:")
        for link in list(set(links))[:5]: # Show unique top 5
            print(f"- {link}")
    print("="*50)

if __name__ == "__main__":
    asyncio.run(test_specific_claim())
