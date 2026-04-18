import requests
from duckduckgo_search import DDGS
from googleapiclient.discovery import build
from google.oauth2 import service_account
from core.config import settings

class Verifier:
    def __init__(self):
        # L6 — Fact verification queries Google Fact Check Tools API
        if settings.GOOGLE_API_KEY:
            self.factcheck_service = build("factchecktools", "v1alpha1", developerKey=settings.GOOGLE_API_KEY)
        else:
            self.google_creds = service_account.Credentials.from_service_account_file(
                settings.GOOGLE_APPLICATION_CREDENTIALS
            )
            self.factcheck_service = build("factchecktools", "v1alpha1", credentials=self.google_creds)

    def verify_ddg(self, query: str):
        try:
            with DDGS() as ddgs:
                return list(ddgs.text(query, max_results=5))
        except Exception as e:
            print(f"Warning: DuckDuckGo search failed: {e}")
            return []

    def verify_google_factcheck(self, query: str):
        """
        Queries Google Fact Check Tools API and returns structured claims.
        Schema: claims[text, claimant, date, reviews[publisher, url, title, date, rating, lang]]
        """
        try:
            request = self.factcheck_service.claims().search(query = query)
            response = request.execute()
            claims = response.get("claims", [])
            
            # Map into the user-requested format for clarity
            results = []
            for c in claims:
                results.append({
                    "text": c.get("text"),
                    "claimant": c.get("claimant"),
                    "claimDate": c.get("claimDate"),
                    "claimReview": c.get("claimReview", [])
                })
            return results
        except Exception as e:
            print(f"Google Fact Check Error: {e}")
            return []

    def verify_wikipedia(self, query: str):
        url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={query}&format=json"
        try:
            res = requests.get(url, timeout = 10).json()
            return res.get("query", {}).get("search", [])
        except:
            return []

    def verify_parallel(self, query: str):
        # Implementation of parallel queries
        return {
            "google": self.verify_google_factcheck(query),
            "wikipedia": self.verify_wikipedia(query),
            "ddg": self.verify_ddg(query)
        }

verifier = Verifier()
