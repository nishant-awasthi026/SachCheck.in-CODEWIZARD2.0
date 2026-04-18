import os
import base64
import io
from sarvamai import SarvamAI
from core.config import settings

class AudioExpert:
    def __init__(self):
        self.api_key = settings.SARVAM_API_KEY
        self.client = None

    def _ensure_client(self):
        if self.client is None:
            if not self.api_key:
                raise ValueError("SARVAM_API_KEY not found in configuration.")
            self.client = SarvamAI(api_subscription_key = self.api_key)

    def transcribe_audio(self, audio_data: str, mode: str = "translate") -> dict:
        """
        Transcribes/Translates audio using Sarvam AI.
        audio_data: Base64 string OR path to file.
        """
        try:
            self._ensure_client()
            
            # 1. Handle Input (Base64 or File Path)
            temp_path = os.path.join(os.environ.get("TEMP", "temp"), "input_audio.wav")
            os.makedirs(os.path.dirname(temp_path), exist_ok = True)
            
            if len(audio_data) < 512 and os.path.exists(audio_data):
                file_to_open = audio_data
            else:
                # Assume Base64
                with open(temp_path, "wb") as f:
                    f.write(base64.b64decode(audio_data))
                file_to_open = temp_path

            # 2. Call Sarvam AI (Saaras v3)
            with open(file_to_open, "rb") as f:
                response = self.client.speech_to_text.transcribe(
                    file = f,
                    model = "saaras:v3",
                    mode = mode # User specifically agreed on "translate"
                )
            
            transcript = response.get("transcript", "")
            
            return {
                "transcript": transcript,
                "language": response.get("language_code"),
                "status": "success"
            }
        except Exception as e:
            return {"status": "error", "message": f"Sarvam AI Error: {str(e)}"}

    def analyze(self, audio_b64: str) -> dict:
        """Compatibility wrapper for standard expert interface."""
        return self.transcribe_audio(audio_b64)

audio_expert = AudioExpert()
