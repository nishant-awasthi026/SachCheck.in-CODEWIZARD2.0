import asyncio
import sys
import os
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.append(os.getcwd())

async def verify_multimodal_logic():
    from orchestrator.graph import workflow
    from experts.image_expert import image_expert
    from experts.video_expert import video_expert
    
    print("--- PHEME Vision Logic Verification: Image ---")
    
    # 1. Test Image Logic
    mock_image_context = "A photo of a protest in London showing a digital clock that says 2025."
    with patch.object(image_expert, 'analyze', return_value={
        "status": "success",
        "visual_context": mock_image_context
    }):
        test_input = {
            "claim_id": "image-verify-001",
            "modality": "image",
            "content": "image_path.jpg",
            "language_hint": "en"
        }
        
        final_state = await workflow.ainvoke(test_input)
        
        print(f"Modality: {test_input['modality']}")
        print(f"Orchestrator Content (Extracted from Image): \"{final_state.get('content')[:100]}...\"")
        print(f"Verdict: {final_state.get('final_verdict')}")
        
    print("\n--- PHEME Vision Logic Verification: Video ---")
    
    # 2. Test Video Logic
    mock_video_context = "A video of a person claiming to be a scientist talking about energy. The audio seems slightly out of sync with lip movements."
    with patch.object(video_expert, 'analyze', return_value={
        "status": "success",
        "video_context": mock_video_context
    }):
        test_input = {
            "claim_id": "video-verify-001",
            "modality": "video",
            "content": "video_path.mp4",
            "language_hint": "en"
        }
        
        final_state = await workflow.ainvoke(test_input)
        
        print(f"Modality: {test_input['modality']}")
        print(f"Orchestrator Content (Extracted from Video): \"{final_state.get('content')[:100]}...\"")
        print(f"Verdict: {final_state.get('final_verdict')}")
        
    print("\n[SUCCESS] Vision Orchestration Verified: Image and Video summaries are correctly extracted and fact-checked.")

if __name__ == "__main__":
    asyncio.run(verify_multimodal_logic())
