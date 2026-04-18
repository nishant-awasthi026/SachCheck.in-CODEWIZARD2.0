import os
from googleapiclient.discovery import build
from core.config import settings

def test_google_raw():
    service = build("factchecktools", "v1alpha1", developerKey=settings.GOOGLE_API_KEY)
    
    queries = ["Earth is flat", "EARTH IS NOT FLAT", "Narendra Modi"]
    
    for q in queries:
        print(f"\nTesting Query: {q}")
        try:
            request = service.claims().search(query=q)
            response = request.execute()
            claims = response.get("claims", [])
            print(f"Found {len(claims)} claims.")
            if claims:
                for c in claims[:1]:
                    print(f"Sample Claim: {c.get('text')}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_google_raw()
