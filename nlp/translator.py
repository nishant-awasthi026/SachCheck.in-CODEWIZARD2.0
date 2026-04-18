import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from core.config import settings
import requests

class Translator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_name_indic_en = "ai4bharat/indictrans2-indic-en-1B"
        self.model_name_en_indic = "ai4bharat/indictrans2-en-indic-1B"
        
        # Using a lazy loading strategy to save VRAM (4GB limit)
        self.indic_en_tokenizer = None
        self.indic_en_model = None
        self.en_indic_tokenizer = None
        self.en_indic_model = None

    def _load_indic_en(self):
        if self.indic_en_model is None:
            self.indic_en_tokenizer = AutoTokenizer.from_pretrained(self.model_name_indic_en, trust_remote_code=True)
            self.indic_en_model = AutoModelForSeq2SeqLM.from_pretrained(
                self.model_name_indic_en, 
                trust_remote_code=True,
                torch_dtype=torch.float16
            ).to(self.device)

    def _load_en_indic(self):
        if self.en_indic_model is None:
            self.en_indic_tokenizer = AutoTokenizer.from_pretrained(self.model_name_en_indic, trust_remote_code=True)
            self.en_indic_model = AutoModelForSeq2SeqLM.from_pretrained(
                self.model_name_en_indic, 
                trust_remote_code=True,
                torch_dtype=torch.float16
            ).to(self.device)

    def translate(self, text: str, src_lang: str, tgt_lang: str) -> str:
        # Fallback to Ollama if VRAM is an issue or for general languages
        if src_lang == "en" and tgt_lang == "en":
            return text
        
        # Specific logic for IndicTrans2 (Hindi/Tamil to English)
        if tgt_lang == "en" and src_lang in ["hi", "ta"]:
            try:
                self._load_indic_en()
                # Simplified preprocessing for demonstration (IndicTransToolkit is better but heavy)
                inputs = self.indic_en_tokenizer(text, return_tensors="pt", padding=True).to(self.device)
                with torch.no_grad():
                    generated_tokens = self.indic_en_model.generate(**inputs, max_length=256)
                return self.indic_en_tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
            except Exception as e:
                print(f"IndicTrans2 Error: {e}. Falling back to Ollama.")
                return self._ollama_translate(text, tgt_lang)
        
        return self._ollama_translate(text, tgt_lang)

    def _ollama_translate(self, text: str, tgt_lang: str) -> str:
        prompt = f"Translate the following text to {tgt_lang}. Respond ONLY with the translation.\n\nText: {text}"
        try:
            response = requests.post(f"{settings.OLLAMA_HOST}/api/generate", json={
                "model": settings.LLM_MODEL,
                "prompt": prompt,
                "stream": False
            })
            if response.status_code == 200:
                return response.json().get("response", text).strip()
        except:
            pass
        return text

translator = Translator()
