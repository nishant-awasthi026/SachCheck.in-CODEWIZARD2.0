import requests
from core.config import settings
from duckduckgo_search import DDGS
import re

class DomainFilter:
    WHITELIST = [
        "timesofindia.indiatimes.com",
        "indiatimes.com",
        "altnews.in",
        "boomlive.in",
        "pib.gov.in",
        "reuters.com",
        "factcheck.afp.com",
        "fullfact.org",
        "snopes.com",
        "thehindu.com",
        "indianexpress.com"
    ]
    
    BLACKLIST = [
        "theonion.com",
        "babylonbee.com",
        "worldnewsdailyreport.com"
    ]

    def is_credible(self, url: str) -> bool:
        if not url: return False
        domain = re.findall(r"://([^/]+)/", url)
        if not domain: return False
        domain = domain[0]
        
        # Check blacklist
        if any(bad in domain for bad in self.BLACKLIST):
            return False
            
        return True
        
    def is_priority(self, url: str) -> bool:
        if not url: return False
        domain = re.findall(r"://([^/]+)/", url)
        if not domain: return False
        domain = domain[0]
        return any(good in domain for good in self.WHITELIST)

class SearchTools:
    def __init__(self):
        self.news_api_key = settings.NEWS_API_KEY
        self.gnews_api_key = settings.GNEWS_API_KEY
        self.guardian_api_key = settings.GUARDIAN_API_KEY
        self.filter = DomainFilter()

    def search_duckduckgo(self, query: str):
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results = 8))
                return results
        except Exception as e:
            print(f"Warning: DuckDuckGo search failed ({e})")
            return []

    def search_news_api(self, query: str):
        if not self.news_api_key:
            return []
        url = f"https://newsapi.org/v2/everything?q={query}&apiKey={self.news_api_key}"
        try:
            res = requests.get(url, timeout = 10).json()
            return res.get("articles", [])[:5]
        except:
            return []

    def search_gnews(self, query: str):
        if not self.gnews_api_key:
            return []
        url = f"https://gnews.io/api/v4/search?q={query}&token={self.gnews_api_key}&lang=en"
        try:
            res = requests.get(url, timeout = 10).json()
            return res.get("articles", [])[:5]
        except:
            return []

    def fetch_all_context(self, query: str):
        """Fetches unified context and filters for credible URLs."""
        all_articles = {
            "news_api": self.search_news_api(query),
            "gnews": self.search_gnews(query),
            "ddg": self.search_duckduckgo(query)
        }
        
        context_str = ""
        links = []
        
        # Process and Filter
        for source, articles in all_articles.items():
            for art in articles:
                url = art.get("url") or art.get("link")
                title = art.get("title") or art.get("body")
                
                if self.filter.is_credible(url):
                    context_str += f"[{source}] {title}\n"
                    links.append(url)
                    
        # Sort links: Whitelisted first
        priority_links = [l for l in links if self.filter.is_priority(l)]
        other_links = [l for l in links if not self.filter.is_priority(l)]
        
        return {
            "context": context_str,
            "links": (priority_links + other_links)[:10]
        }

search_tools = SearchTools()
