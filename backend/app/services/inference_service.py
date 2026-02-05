import joblib
import pandas as pd
import os
import logging

logger = logging.getLogger(__name__)

class RiskPredictor:
    def __init__(self, model_path: str = None):
        self.model = None
        # Try to find model in common locations
        paths = [
            model_path,
            "../ml/models/water_quality_rf.pkl",
            "/app/models/water_quality_rf.pkl", # Docker path
            "ml/models/water_quality_rf.pkl"
        ]
        
        for p in paths:
            if p and os.path.exists(p):
                try:
                    self.model = joblib.load(p)
                    logger.info(f"Loaded ML model from {p}")
                    break
                except Exception as e:
                    logger.error(f"Failed to load model from {p}: {e}")
        
        if not self.model:
            logger.warning("No ML model found. Using heuristic fallback.")

    def predict_risk(self, data: dict) -> int:
        """
        Returns risk level: 0 (Safe), 1 (Warning), 2 (Critical)
        """
        ph = data.get('ph', 7.0)
        turbidity = data.get('turbidity', 5.0)
        temp = data.get('temperature', 25.0)
        tds = data.get('tds', 300.0)

        if self.model:
            try:
                # DataFrame with correct feature names is safer for sklearn
                features = pd.DataFrame([[ph, turbidity, temp, tds]], 
                                      columns=['ph', 'turbidity', 'temperature', 'tds'])
                return int(self.model.predict(features)[0])
            except Exception as e:
                logger.error(f"Prediction error: {e}")
                return self._heuristic(ph, turbidity)
        else:
            return self._heuristic(ph, turbidity)

    def _heuristic(self, ph, turbidity):
        if ph < 6.0 or ph > 9.0 or turbidity > 50:
            return 2
        if ph < 6.5 or ph > 8.5 or turbidity > 10:
            return 1
        return 0

# Global instance
predictor = RiskPredictor()
