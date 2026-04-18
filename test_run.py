import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.models import ClaimRequest
from gateway.api import analyze_claim
from fastapi import BackgroundTasks

async def test_pipeline():
    print("Testing PHEME Fact-Checking Pipeline...")
    
    request = ClaimRequest(
        id="test-123",
        text="The sun is actually made of cheese, NASA confirmed this yesterday.",
        language="en"
    )
    
    bg_tasks = BackgroundTasks()
    
    try:
        result = await analyze_claim(request, bg_tasks)
        print(f"Outcome Verdict: {result.verdict}")
        print(f"Outcome Score: {result.score}")
        print(f"Outcome Confidence: {result.confidence}")
        print(f"Narrative: {result.counter_narrative}")
        print("Integration test successful.")
    except Exception as e:
        print(f"Pipeline failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_pipeline())
