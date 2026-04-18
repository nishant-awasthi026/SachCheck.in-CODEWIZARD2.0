from langgraph.graph import StateGraph, END
from orchestrator.state import FactCheckState
from core.graph_rag import graph_rag
from core.verifier import verifier
from core.tools import search_tools
from core.generator import generator
from experts.text_expert import text_expert
from experts.image_expert import image_expert
from experts.audio_expert import audio_expert
from experts.video_expert import video_expert
import json

# Node 0: Multimodal Processor (Entry Point)
async def multimodal_processor_node(state: FactCheckState):
    # Initialize trace and classifiers
    trace = state.get("trace", [])
    classifiers = state.get("classifiers", [])
    modality = state.get("modality")
    content = state.get("content")
    
    if modality == "text":
        return {"original_text": content, "trace": ["Entry: Text Input"], "classifiers": ["Text Expert"]}
        
    print(f"\n[Stage 0] Processing Multimodal Input: {modality.upper()}...")
    trace.append(f"Pre-Process: {modality.upper()} Translation")
    classifiers.append(f"{modality.capitalize()} Expert")
    
    if modality == "audio":
        result = audio_expert.transcribe_audio(content, mode="translate")
        if result["status"] == "success":
            return {
                "original_text": result["transcript"],
                "content": result["transcript"],
                "analysis_results": {"audio": result},
                "trace": trace,
                "classifiers": classifiers
            }
            
    elif modality == "image":
        result = image_expert.analyze(content) 
        if result["status"] == "success":
            return {
                "original_text": result["visual_context"],
                "content": result["visual_context"],
                "analysis_results": {"image": result},
                "trace": trace,
                "classifiers": classifiers
            }
            
    elif modality == "video":
        result = video_expert.analyze(content)
        if result["status"] == "success":
            return {
                "original_text": result["video_context"],
                "content": result["video_context"],
                "analysis_results": {"video": result},
                "trace": trace,
                "classifiers": classifiers
            }

    # Handle errors
    error_msg = result.get("message") if 'result' in locals() else "Unknown modality"
    trace.append(f"ERROR: {error_msg}")
    return {
        "final_verdict": "ERROR", 
        "explanation": f"{modality.upper()} processing failed: {error_msg}",
        "trace": trace,
        "flagging": "CRITICAL"
    }

# Node 1: Pre-Verify (Google Fact Check Search)
async def pre_verify_node(state: FactCheckState):
    # Check if we already hit an error in audio processing
    if state.get("final_verdict") == "ERROR":
        return state

    print("\n[Stage 1] Pre-Verifying with Google Fact Check API...")
    content = state["content"]
    results = verifier.verify_google_factcheck(content)
    
    trace = state.get("trace", [])
    trace.append("Stage 1: Google Fact-Check API Search")
    
    links = []
    if results:
        for claim in results:
            if "claimReview" in claim:
                for review in claim["claimReview"]:
                    if "url" in review:
                        links.append(review["url"])
                        
    return {"pre_verify_results": {"claims": results}, "links": links, "trace": trace}

# Router: Decide between Synthesis and Orchestrator Discussion
def route_after_pre_verify(state: FactCheckState):
    results = state.get("pre_verify_results", {}).get("claims")
    return "synthesize" if results else "orchestrate"

# Node 2a: Synthesize Verdict (If Google Fact Check matches)
async def synthesize_node(state: FactCheckState):
    print("\n[Stage 2] Synthesizing verdict from existing fact-checks...")
    claims = state["pre_verify_results"]["claims"]
    user_claim = state["content"]
    
    prompt = f"""
    You are a Fact-Check Synthesizer. 
    User Claim: "{user_claim}"
    
    Verified Reports Found:
    {json.dumps(claims, indent=2)}
    
    INSTRUCTION:
    1. Compare the User Claim against the Verified Reports.
    2. BE CAREFUL with negation. (e.g., If a report says "X is false", and the User Claim is "X is not true", then the User is REAL).
    3. Determine if the User's specific statement is REAL, FAKE, or MISLEADING.
    
    Format JSON strictly:
    {{
        "verdict": "REAL" | "FAKE" | "MISLEADING",
        "explanation": "Detailed explanation of why this verdict was reached, referencing the reports.",
        "counter_narrative": "A concise, factual statement providing the correct information if the claim is false or misleading. If REAL, provide a reinforcing factual statement."
    }}
    """
    
    # Use text_expert with a custom prompt to avoid nesting
    synthesis = text_expert.analyze_claim(user_claim, custom_prompt = prompt)
    
    return {
        "final_verdict": synthesis.get("verdict"),
        "explanation": synthesis.get("explanation"),
        "counter_narrative": synthesis.get("counter_narrative"),
        "links": state.get("links", []),
        "analysis_results": synthesis
    }

# Node 2b: AI Orchestrator Discussion (If no fact-checks found)
async def orchestrator_discussion_node(state: FactCheckState):
    print("\n[Stage 2] AI Orchestrator Discussion Initiated (3 Agents)...")
    content = state["content"]
    trace = state.get("trace", [])
    trace.append("Stage 2: Multi-Agent Contextual Discussion")

    # 1. Fetch live context
    search_data = search_tools.fetch_all_context(content)
    context_str = search_data.get("context", "")
    links = search_data.get("links", [])
    
    # 2. Fetch graph context
    graph_results = await graph_rag.search(content)
    
    # 3. Discussion
    discussion_prompt = f"""
    The following agents are discussing a claim:
    Claim: "{content}"
    
    Evidence Found:
    Web Search: {context_str}
    Graph Context: {graph_results}
    
    GOAL: Contextualize, explain, and counter misinformation in real time.
    Generate a trustworthy summary, highlight inconsistencies, and provide verifiable alternatives.
    
    Format JSON strictly:
    {{
        "verdict": "REAL" | "FAKE" | "MISLEADING",
        "confidence": 0.0 to 1.0,
        "inconsistencies": ["list specific factual clashes"],
        "flagging": "SAFE" | "WARNING" | "CRITICAL",
        "counter_narrative": "Detailed alternative verifiable info",
        "explanation": "Summarized trustworthy decision"
    }}
    """
    
    decision = text_expert.analyze_claim(content, custom_prompt = discussion_prompt)
    
    return {
        "final_verdict": decision.get("verdict"),
        "explanation": decision.get("explanation"),
        "counter_narrative": decision.get("counter_narrative"),
        "confidence": decision.get("confidence", 0.5),
        "flagging": decision.get("flagging", "WARNING"),
        "inconsistencies": decision.get("inconsistencies", []),
        "links": links,
        "trace": trace
    }

async def finalize_node(state: FactCheckState):
    print("\n[Stage 3] Finalizing result...")
    
    # Store in memory for future RAG
    print("--- Updating Knowledge Graph ---")
    await graph_rag.cognify_claim(
        state["claim_id"], 
        state["content"],
        verdict = state.get("final_verdict"),
        explanation = state.get("explanation"),
        counter_narrative = state.get("counter_narrative")
    )
    
    return state

# Workflow Definition
builder = StateGraph(FactCheckState)

builder.add_node("multimodal_processor", multimodal_processor_node)
builder.add_node("pre_verify", pre_verify_node)
builder.add_node("synthesize", synthesize_node)
builder.add_node("orchestrate", orchestrator_discussion_node)
builder.add_node("finalize", finalize_node)

builder.set_entry_point("multimodal_processor")
builder.add_edge("multimodal_processor", "pre_verify")
builder.add_conditional_edges(
    "pre_verify", 
    route_after_pre_verify, 
    {"synthesize": "synthesize", "orchestrate": "orchestrate"}
)
builder.add_edge("synthesize", "finalize")
builder.add_edge("orchestrate", "finalize")
builder.add_edge("finalize", END)

workflow = builder.compile()
