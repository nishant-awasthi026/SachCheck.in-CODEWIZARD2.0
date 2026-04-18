class Scorer:
    def __init__(self):
        # Weighted combination of 7 signals including a temporal drift penalty.
        self.weights = {
            "text_logic": 0.20,
            "evidence_match": 0.25,
            "source_reliability": 0.15,
            "multimodal_consistency": 0.10,
            "deepfake_penalty": 0.15,
            "temporal_drift": 0.05,
            "verification_signal": 0.10
        }

    def calculate_score(self, signals: dict) -> float:
        score = 0.0
        
        # 1. Text Logic (0-1)
        score += signals.get("text_logic", 0.5) * self.weights["text_logic"]
        
        # 2. Evidence Match (0-1)
        score += signals.get("evidence_match", 0) * self.weights["evidence_match"]
        
        # 3. Source Reliability (0-1)
        score += signals.get("source_reliability", 0) * self.weights["source_reliability"]
        
        # 4. Multi-modal Consistency (0-1)
        score += signals.get("multimodal_consistency", 0.5) * self.weights["multimodal_consistency"]
        
        # 5. Deepfake Penalty (High Synthetic = Low Score)
        deepfake_signal = 1.0 - signals.get("deepfake_signal", 0)
        score += deepfake_signal * self.weights["deepfake_penalty"]
        
        # 6. Temporal Drift Penalty (High Variance = Low Score)
        drift_penalty = max(0, 1.0 - signals.get("temporal_drift", 0) * 10)
        score += drift_penalty * self.weights["temporal_drift"]
        
        # 7. Verification Signal (supports vs contradicts)
        score += signals.get("verification_signal", 0.5) * self.weights["verification_signal"]

        return round(min(max(score, 0.0), 1.0), 2)

scorer = Scorer()
