import time
import os
from google import genai
from core.config import settings

class VideoExpert:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.client = None

    def _ensure_client(self):
        if self.client is None:
            if not self.api_key:
                raise ValueError("GEMINI_API_KEY not found in configuration.")
            self.client = genai.Client(api_key = self.api_key)

    def analyze_video(self, file_path: str):
        """
        Analyzes a video for deepfake signs and temporal context using Gemini 1.5 Flash.
        """
        print(f"Uploading video to Gemini: {file_path}")
        try:
            self._ensure_client()
            
            # 1. Upload
            video_file = self.client.files.upload(file = file_path)
            print(f"Uploaded as: {video_file.name}. Waiting for frame extraction...")
            
            # 2. Polling
            while video_file.state.name == "PROCESSING":
                print(".", end = "", flush = True)
                time.sleep(2)
                video_file = self.client.files.get(name = video_file.name)
                
            if video_file.state.name == "FAILED":
                return {"status": "error", "message": "Google failed to process the video."}
                
            print("\nVideo processed! Running AI analysis...")
            
            # 3. Analyze
            prompt = """
            Watch this video carefully for fact-checking purposes.
            1. Provide a timestamped summary of events.
            2. Does the audio match the lip movements?
            3. Are there unnatural movements or glitches indicating a deepfake?
            Summarize the findings clearly.
            """
            
            response = self.client.models.generate_content(
                model = "gemini-1.5-flash",
                contents = [prompt, video_file]
            )
            
            # 4. Cleanup
            self.client.files.delete(name = video_file.name)
            print("Video analysis complete and file deleted from Gemini servers.")
            
            return {
                "video_context": response.text,
                "status": "success"
            }
        except Exception as e:
            print(f"Video Error: {e}")
            return {"status": "error", "message": str(e)}

    def analyze(self, video_url: str, claim_text: str = ""):
        """Compatibility wrapper for standard expert interface."""
        return self.analyze_video(video_url)

video_expert = VideoExpert()
