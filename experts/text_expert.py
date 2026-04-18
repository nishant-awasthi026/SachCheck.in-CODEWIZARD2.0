from groq import Groq
import json
from core.config import settings

class TextExpert:
    def __init__(self):
        self.client = Groq(api_key = settings.GROQ_API_KEY)
        self.model = settings.LLM_MODEL
        if self.model.startswith("groq/"):
            self.model = self.model.replace("groq/", "")

    def analyze_claim(self, claim: str, context: str = "", custom_prompt: str = None) -> dict:
        if custom_prompt:
            prompt = custom_prompt
        else:
            prompt = f"""
            You are a highly capable misinformation detection expert.
            Analyze the following claim for logical fallacies, factual inaccuracies, and tone.
            
            Context evidence retrieved from databases: {context}
            Claim: "{claim}"
            
            Provide your analysis in the following JSON format strictly:
            {{
                "verdict": "REAL" | "FAKE" | "MISLEADING" | "NEI",
                "confidence": 0.0 to 1.0,
                "fallacies": ["list any logical fallacies found"],
                "explanation": "Brief explanation of your verdict",
                "detected_claims": ["list of atomic claims made in the text"]
            }}
            """

        try:
            completion = self.client.chat.completions.create(
                model = self.model,
                messages = [
                    {"role": "user", "content": prompt}
                ],
                temperature = 0, # Low temperature for consistent analysis
                max_completion_tokens = 1024,
                top_p = 1,
                stream = False,
                # Using the user provided compound_custom pattern
                compound_custom = {"tools": {"enabled_tools": ["web_search", "code_interpreter", "visit_website"]}}
            )
            
            content = completion.choices[0].message.content
            # Filter out potential markdown blocks if LLM adds them
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
                
            return json.loads(content)
        except Exception as e:
            print(f"TextExpert Error: {e}")
            return {"verdict": "NEI", "confidence": 0.0, "error": str(e)}

text_expert = TextExpert()
