import redis
import hashlib
import json
from core.config import settings

class FingerprintAgent:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST, 
            port=settings.REDIS_PORT, 
            decode_responses=True
        )

    def get_fingerprint(self, modality: str, content: str) -> str:
        # Create a unique hash for the claim
        raw_string = f"{modality}:{content}"
        return hashlib.sha256(raw_string.encode()).hexdigest()

    def check_cache(self, fingerprint: str):
        try:
            # L3 — if it hits the Redis cache, the entire inference pipeline 
            # is bypassed and a stored verdict is returned in under 10ms.
            cached_result = self.redis_client.get(f"claim:{fingerprint}")
            if cached_result:
                return json.loads(cached_result)
        except redis.exceptions.ConnectionError:
            print("Warning: Redis not connected. Bypassing cache.")
        return None

    def cache_verdict(self, fingerprint: str, result: dict, ttl: int = 86400):
        try:
            self.redis_client.setex(
                f"claim:{fingerprint}", 
                ttl, 
                json.dumps(result)
            )
        except redis.exceptions.ConnectionError:
            pass

fingerprint_agent = FingerprintAgent()
