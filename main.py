import os
import uuid
import shutil
from typing import List, Optional
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from orchestrator.graph import workflow
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="PHEME Multimodal Fact-Checking API",
    description="A high-fidelity multimodal misinformation detection and counter-narrative orchestration engine.",
    version="1.0.0"
)

# Enable CORS for the future frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Storage Config (D: drive isolation)
UPLOAD_DIR = r"D:\PHEME\uploads"
os.makedirs(UPLOAD_DIR, exist_ok = True)

class FactCheckResponse(BaseModel):
    CLAIM: str
    TRUTH: str
    EXPLAINATION: str
    flagging: str
    countering_misinformation: str
    classifiers: List[str]
    automated_fact_verification_pipeline: List[str]
    credibility_scoring_mechanism: float
    inconsistencies: List[str]
    links: List[str]

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "PHEME"}

@app.post("/verify/text", response_model = FactCheckResponse)
async def verify_text(claim: str = Form(...), language: str = Form("en")):
    """
    Verifies a text-only claim.
    """
    input_data = {
        "claim_id": str(uuid.uuid4()),
        "modality": "text",
        "content": claim,
        "language_hint": language
    }
    
    try:
        final_state = await workflow.ainvoke(input_data)
        return format_response(final_state)
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))

@app.post("/verify/multimodal", response_model = FactCheckResponse)
async def verify_multimodal(
    file: UploadFile = File(...),
    language: str = Form("en")
):
    """
    Verifies a file upload (Image, Video, or Audio).
    The system automatically detects the modality.
    """
    file_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[1]
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}{ext}")
    
    # Identify modality by extension
    modality = "text"
    if ext.lower() in [".jpg", ".jpeg", ".png", ".webp"]:
        modality = "image"
    elif ext.lower() in [".mp4", ".mov", ".avi", ".mkv"]:
        modality = "video"
    elif ext.lower() in [".wav", ".mp3", ".m4a", ".flac"]:
        modality = "audio"
    else:
        raise HTTPException(status_code = 400, detail = f"Unsupported file extension: {ext}")

    # Save file to D: drive
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    input_data = {
        "claim_id": file_id,
        "modality": modality,
        "content": file_path,
        "language_hint": language
    }
    
    try:
        final_state = await workflow.ainvoke(input_data)
        # Cleanup temp file if needed (optional, keeping for now for RAG context)
        return format_response(final_state)
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))

def format_response(state):
    """
    Maps LangGraph state to the user's requested output parameters.
    """
    return {
        "CLAIM": state.get("original_text", state.get("content", "N/A")),
        "TRUTH": state.get("final_verdict", "UNKNOWN"),
        "EXPLAINATION": state.get("explanation", "No explanation provided."),
        "flagging": state.get("flagging", "WARNING"),
        "countering_misinformation": state.get("counter_narrative", "N/A"),
        "classifiers": state.get("classifiers", ["General Classifier"]),
        "automated_fact_verification_pipeline": state.get("trace", ["Logic Engine"]),
        "credibility_scoring_mechanism": state.get("confidence", 0.0),
        "inconsistencies": state.get("inconsistencies", []),
        "links": list(set(state.get("links", [])))
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host = "0.0.0.0", port = 8000)
