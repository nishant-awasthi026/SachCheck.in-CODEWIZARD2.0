from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ClaimRequest(BaseModel):
    id: str
    modality: str  # text, image, audio, video
    content: str  # text content or base64 data / url
    language_hint: str = "en"
    source_url: Optional[str] = None
    metadata: Dict[str, Any] = {}

class FactCheckResult(BaseModel):
    score: float
    verdict: str  # REAL, FAKE, MISLEADING, NEI
    confidence: float
    explanation: str
    counter_narrative: str
    source_links: List[str]
    metadata: Dict[str, Any]
