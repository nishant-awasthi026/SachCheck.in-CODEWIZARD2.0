from typing import TypedDict, List, Dict, Any, Optional

class FactCheckState(TypedDict):
    claim_id: str
    modality: str      # Added: "text", "image", etc.
    content: str       # Added: raw text or b64 image
    original_text: str
    
    # Internal markers
    is_cached: bool    # Added: for conditional routing
    fingerprint: str   # Added: unique ID from fingerprint node
    
    # Context Evidence
    qdrant_context: Optional[str]
    neo4j_context: Optional[str]
    
    # Analysis & Verification results
    analysis_results: Dict[str, Any] # Changed from text_analysis
    verifications: Dict[str, Any]
    
    # Final Verdict Card
    final_verdict: Optional[str]
    score: float
    explanation: str
    links: List[str]
    # New fields for Google Fact Check and Discussion logic
    pre_verify_results: Optional[Dict[str, Any]]
    discussion_history: List[Dict[str, str]] 
    counter_narrative: Optional[str]
    
    # New Production/Frontend Fields
    confidence: float          # Credibility score (0-1)
    flagging: str              # categorical: "SAFE", "WARNING", "CRITICAL"
    trace: List[str]           # Pipeline step log
    classifiers: List[str]     # Experts used
    inconsistencies: List[str] # List of contradictions found
    
    language_hint: str
