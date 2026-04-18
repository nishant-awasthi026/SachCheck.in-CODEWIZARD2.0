import os
import sys
from googleapiclient.discovery import build
from google.oauth2 import service_account

sys.path.append(os.getcwd())
from core.config import settings

def debug_google_v2():
    creds = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_APPLICATION_CREDENTIALS
    )
    service = build("factchecktools", "v1alpha1", credentials=creds)
    
    query = "modi" # Simpler query to test if it's the specific text
    print(f"Testing simple query: {query}")
    try:
        # Some versions/accounts require at least 1 language code or specific pageSize
        request = service.claims().search(query=query, languageCode="en")
        response = request.execute()
        print("Success with languageCode!")
    except Exception as e:
        print(f"Failed with languageCode: {e}")
        try:
            request = service.claims().search(query=query)
            response = request.execute()
            print("Success with basic query!")
        except Exception as e2:
            print(f"Final failure: {e2}")

if __name__ == "__main__":
    debug_google_v2()
