import os
import PIL.Image
import base64
from google import genai
from core.config import settings

class ImageExpert:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.client = None

    def _ensure_client(self):
        if self.client is None:
            if not self.api_key:
                raise ValueError("GEMINI_API_KEY not found in configuration.")
            self.client = genai.Client(api_key = self.api_key)

    def analyze_image(self, file_path: str):
        """
        Analyzes an image for context, anomalies, and OCR text using Gemini 1.5 Flash.
        """
        print(f"Analyzing image: {file_path}")
        try:
            self._ensure_client()
            img = PIL.Image.open(file_path)
            
            prompt = """
            Analyze this image for fact-checking purposes.
            1. Describe the scene and context.
            2. Are there any visual anomalies or signs of AI generation/Photoshop?
            3. Extract any visible text in the image.
            Return the analysis in a structured, concise format.
            """
            
            response = self.client.models.generate_content(
                model = "gemini-1.5-flash",
                contents = [prompt, img]
            )
            
            print("Image analysis complete!")
            return {
                "visual_context": response.text,
                "status": "success"
            }
        except Exception as e:
            print(f"Image Error: {e}")
            return {"status": "error", "message": str(e)}

    def analyze(self, image_b64: str, claim_text: str = ""):
        """Compatibility wrapper for standard expert interface."""
        # Check if it's already a path
        if os.path.exists(image_b64):
            return self.analyze_image(image_b64)
            
        temp_path = os.path.join(os.environ.get("TEMP", "temp"), "input_image.jpg")
        os.makedirs(os.path.dirname(temp_path), exist_ok = True)
        
        try:
            with open(temp_path, "wb") as f:
                f.write(base64.b64decode(image_b64))
            return self.analyze_image(temp_path)
        except Exception as e:
            return {"status": "error", "message": f"Base64 decode error: {str(e)}"}

image_expert = ImageExpert()
