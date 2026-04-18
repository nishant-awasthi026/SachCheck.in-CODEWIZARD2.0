import sys
import os
import importlib

# Add project root to path
sys.path.append(os.getcwd())

try:
    print("Testing imports...")
    from gateway.api import app
    from orchestrator.graph import workflow
    from core.config import settings
    from nlp.translator import translator
    from nlp.embeddings import embedder
    from experts.image_expert import image_expert
    from experts.audio_expert import audio_expert
    from experts.video_expert import video_expert
    from core.graph_rag import graph_rag
    from core.verifier import verifier
    from core.scorer import scorer
    from core.generator import generator
    
    print("\nSUCCESS: All layers imported successfully!")
    print(f"App: {settings.APP_NAME} v{settings.APP_VERSION}")
    
    import torch
    print(f"CUDA Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
    
except Exception as e:
    print(f"\nFAILURE: Import test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
