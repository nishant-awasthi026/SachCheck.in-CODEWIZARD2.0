import requests
import json
import os

def test_api():
    print("--- Verifying PHEME Production API ---")
    
    # 1. Test Text Verification
    print("\n[TEST 1] Text Verification...")
    text_data = {
        "claim": "Water boils at 100 degrees Celsius at sea level.",
        "language": "en"
    }
    response = requests.post("http://localhost:8000/verify/text", data=text_data)
    
    if response.status_code == 200:
        res = response.json()
        print("✅ API Response Schema Valid")
        print(f"CLAIM: {res['CLAIM']}")
        print(f"TRUTH: {res['TRUTH']}")
        print(f"PIPELINE: {res['automated_fact_verification_pipeline']}")
        print(f"CONFIDENCE: {res['credibility_scoring_mechanism']}")
    else:
        print(f"❌ Text Verification Failed: {response.text}")

    # 2. Test Multimodal Verification (Image)
    image_path = r"D:\Downloads\check it.jpg"
    if os.path.exists(image_path):
        print("\n[TEST 2] Multimodal Verification (Image)...")
        with open(image_path, "rb") as f:
            files = {"file": f}
            response = requests.post("http://localhost:8000/verify/multimodal", files=files)
            
        if response.status_code == 200:
            res = response.json()
            print("✅ API Multimodal Response Schema Valid")
            print(f"CLAIM (Extracted): {res['CLAIM'][:50]}...")
            print(f"COUNTER-MISINFO: {res['countering_misinformation']}")
            print(f"INCONSISTENCIES: {res['inconsistencies']}")
        else:
            print(f"❌ Multimodal Verification Failed: {response.text}")
    else:
        print("\n[SKIP] Multimodal test skipped: check it.jpg not found.")

if __name__ == "__main__":
    test_api()
