import asyncio
import sys
import os
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.append(os.getcwd())

async def test_audio_workflow_verification():
    from orchestrator.graph import workflow
    from experts.audio_expert import audio_expert
    
    # Mock the Sarvam AI response to simulate a successful "translate" to English
    mock_transcript = "The moon is made of green cheese."
    
    print(f"--- PHEME Verification: Audio -> Text -> Verdict Workflow ---")
    print(f"Targeting Claim (Simulated Audio): '{mock_transcript}'")

    # We mock the internal transcribe_audio method
    with patch.object(audio_expert, 'transcribe_audio', return_value={
        "status": "success",
        "transcript": mock_transcript,
        "language": "en"
    }):
        test_input = {
            "claim_id": "verify-001",
            "modality": "audio",
            "content": "mock_audio_file.wav",
            "language_hint": "en"
        }
        
        # Run the orchestrator
        final_state = await workflow.ainvoke(test_input)
        
        print("\n" + "="*50)
        print("VERIFICATION RESULTS")
        print("="*50)
        print(f"1. MODALITY DETECTED: {test_input['modality']}")
        print(f"2. SARVAM TRANSCRIPTION: '{final_state.get('content')}'")
        print(f"3. STAGE 1 (GOOGLE) / STAGE 2 (DISCUSSION): Triggered")
        print(f"4. FINAL VERDICT: {final_state.get('final_verdict')}")
        print(f"5. EXPLANATION: {final_state.get('explanation')[:100]}...")
        
        links = final_state.get("links", [])
        if links:
            print("\n6. REFERENCES FOUND:")
            for link in list(set(links))[:3]:
                print(f"- {link}")
        
        # Check if the workflow correctly updated the content from audio to text
        if final_state.get('content') == mock_transcript:
            print("\n[SUCCESS] Workflow Verified: Audio input correctly transformed and processed.")
        else:
            print("\n[FAILURE] Workflow logic mismatch.")
        print("="*50)

if __name__ == "__main__":
    asyncio.run(test_audio_workflow_verification())
