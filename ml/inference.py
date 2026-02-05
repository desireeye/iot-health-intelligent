import joblib
import pandas as pd
import os
import numpy as np

class RiskPredictor:
    def __init__(self, model_path="ml/models/water_quality_rf.pkl"):
        # In a real app, use absolute paths or env vars
        # Fallback for dev environment where we might run from root or backend
        if not os.path.exists(model_path):
             # Try relative to package
             model_path = os.path.join(os.path.dirname(__file__), "models/water_quality_rf.pkl")
             
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
            print(f"Loaded ML Model from {model_path}")
        else:
            print(f"Model not found at {model_path}. Using dummy predictor.")
            self.model = None

    def predict(self, ph, turbidity, temperature, tds):
        if not self.model:
            # Dummy logic if model not trained yet
            if ph < 6 or ph > 8.5 or turbidity > 10:
                return 2 # High Risk
            return 0
        
        features = pd.DataFrame([[ph, turbidity, temperature, tds]], 
                                columns=['ph', 'turbidity', 'temperature', 'tds'])
        prediction = self.model.predict(features)[0]
        # prediction is 0, 1, 2
        return int(prediction)

    def get_risk_label(self, risk_level):
        mapping = {0: "SAFE", 1: "WARNING", 2: "CRITICAL"}
        return mapping.get(risk_level, "UNKNOWN")
