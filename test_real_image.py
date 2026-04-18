import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

# Ensure UTF-8 output for Windows console (to handle Unicode from Gemini)
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

async def verify_real_image():
    from orchestrator.graph import workflow
    
    image_path = r"D:\Downloads\check it.jpg"
    
    test_input = {
        "claim_id": "real-image-verify",
        "modality": "image",
        "content": image_path,
        "language_hint": "en"
    }
    
    print(f"--- PHEME Real-World Verification: {image_path} ---")
    
    try:
        final_state = await workflow.ainvoke(test_input)
        
        print("\n" + "="*50)
        print("REAL-WORLD IMAGE VERIFICATION RESULTS")
        print("="*50)
        
        # 1. Show the Image Analysis (OCR/Description)
        analysis = final_state.get("analysis_results", {}).get("image", {})
        visual_context = analysis.get("visual_context", "No analysis found.")
        
        print(f"IMAGE-TO-TEXT ANALYSIS:\n{visual_context}\n")
        
        # 2. Show the Verdict
        print(f"FINAL VERDICT: {final_state.get('final_verdict')}")
        print(f"EXPLANATION: {final_state.get('explanation')}")
        print(f"COUNTER-NARRATIVE: {final_state.get('counter_narrative')}")
        
        links = final_state.get("links", [])
        if links:
            print("\nVERIFICATION SOURCES:")
            for link in list(set(links))[:5]:
                print(f"- {link}")
        print("="*50)
        
    except Exception as e:
        print(f"Verification failed: {e}")

if __name__ == "__main__":
    asyncio.run(verify_real_image())
