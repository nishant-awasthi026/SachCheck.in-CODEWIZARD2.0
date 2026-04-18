import os
import sys
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Force path
sys.path.append(os.getcwd())
from core.config import settings

def debug_google():
    print(f"Creds path: {settings.GOOGLE_APPLICATION_CREDENTIALS}")
    creds = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_APPLICATION_CREDENTIALS
    )
    service = build("factchecktools", "v1alpha1", credentials=creds)
    
    query = "modi ji have tasted dog meat"
    print(f"Testing query: {query}")
    try:
        # Standard search
        request = service.claims().search(query=query)
        response = request.execute()
        print("Success!")
        print(response)
    except Exception as e:
        print(f"Error caught: {e}")
        # Try without service account if public? 
        # (Though most Google APIs need at least a key)

if __name__ == "__main__":
    debug_google()
