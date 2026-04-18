from nlp.translator import translator

class CardGenerator:
    def __init__(self):
        pass

    def generate_fact_card(self, data: dict, original_language: str) -> dict:
        # L7 — produces a structured fact card in the original language, 
        # with the verdict, inconsistency explanation, and 2-3 verifiable source links.
        
        verdict = data.get("verdict", "NEI")
        explanation = data.get("explanation", "")
        links = data.get("links", [])[:3]
        
        # Translate to original language if not English
        if original_language != "en":
            translated_verdict = translator.translate(verdict, "en", original_language)
            translated_explanation = translator.translate(explanation, "en", original_language)
        else:
            translated_verdict = verdict
            translated_explanation = explanation

        return {
            "verdict": translated_verdict,
            "explanation": translated_explanation,
            "source_links": links,
            "credibility_score": data.get("score", 0.0),
            "original_language": original_language,
            "fact_card_id": f"FC-{hash(translated_explanation) % 10000}"
        }

generator = CardGenerator()
