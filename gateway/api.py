from fastapi import FastAPI, HTTPException, BackgroundTasks
from core.models import ClaimRequest, FactCheckResult
from core.config import settings
from orchestrator.graph import workflow

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

@app.get("/")
def read_root():
    return {"status": "online", "app": settings.APP_NAME, "version": settings.APP_VERSION}

@app.post("/analyze", response_model=FactCheckResult)
async def analyze_claim(request: ClaimRequest, background_tasks: BackgroundTasks):
    try:
        initial_state = {
            "claim_id": request.id,
            "modality": request.modality,
            "content": request.content,
            "source_url": request.source_url,
            "language_hint": request.language_hint,
            "metadata": request.metadata,
            "original_text": "",
            "translated_text": "",
            "source_language": request.language_hint,
            "qdrant_context": [],
            "neo4j_context": [],
            "analysis_results": {},
            "verifications": [],
            "final_verdict": "NEI",
            "confidence": 0.0,
            "explanation": "",
            "counter_narrative": "",
            "score": 0.0
        }
        
        # Run LangGraph Orchestration Async
        result = await workflow.ainvoke(initial_state)
        
        return FactCheckResult(
            score=result.get("score", 0.0),
            verdict=result.get("final_verdict", "NEI"),
            confidence=result.get("confidence", 0.0),
            explanation=result.get("explanation", ""),
            counter_narrative=result.get("counter_narrative", ""),
            source_links=result.get("source_links", []),
            metadata=result.get("metadata", {})
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
