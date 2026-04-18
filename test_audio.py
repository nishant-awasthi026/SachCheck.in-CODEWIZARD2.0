import asyncio
import sys
import os
import base64

# Add project root to path
sys.path.append(os.getcwd())

async def test_audio_input():
    from orchestrator.graph import workflow
    
    # We will "mock" a b64 string that conceptually represents audio
    # In a real test, you'd provide a path to a .wav file
    audio_path = "test_audio.wav"
    
    # Create a dummy audio file if it doesn't exist
    if not os.path.exists(audio_path):
        with open(audio_path, "wb") as f:
            f.write(b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x44\xac\x00\x00\x88\x58\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00")
    
    test_input = {
        "claim_id": "audio-test-001",
        "modality": "audio",
        "content": audio_path, # Passing the path
        "language_hint": "hi"
    }
    
    print(f"--- PHEME Multimodal Test: Audio Input via Sarvam AI ---")
    
    # Run the orchestrator
    try:
        final_state = await workflow.ainvoke(test_input)
        
        print("\n" + "="*50)
        print("FINAL ORCHESTRATOR DECISION (FROM AUDIO)")
        print("="*50)
        print(f"TRANSCRIBED TEXT: {final_state.get('content')}")
        print(f"VERDICT: {final_state.get('final_verdict')}")
        print(f"EXPLANATION: {final_state.get('explanation')}")
        print(f"COUNTER-NARRATIVE: {final_state.get('counter_narrative')}")
        
        links = final_state.get("links", [])
        if links:
            print("\nREFERENCES:")
            for link in list(set(links))[:5]:
                print(f"- {link}")
        print("="*50)
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_audio_input())
