# 📁 services/supervised_model.py
import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

class MultiModelFraudDetector:
    def __init__(self):
        self.models = {}
        self.columns = [
            'Avg min between sent tnx', 'Avg min between received tnx',
            'Time Diff between first and last (Mins)', 'Sent tnx', 'Received Tnx',
            'Number of Created Contracts', 'max value received ',
            'avg val received', 'avg val sent',
            'total Ether sent', 'total ether balance',
            ' ERC20 total Ether received', ' ERC20 total ether sent',
            ' ERC20 total Ether sent contract', ' ERC20 uniq sent addr',
            ' ERC20 uniq rec token name'
        ]

    def load_models(self):
        with open("models_ml/logistic_model.pkl", "rb") as f:
            self.models["logistic"] = pickle.load(f)
        with open("models_ml/random_forest_model.pkl", "rb") as f:
            self.models["random_forest"] = pickle.load(f)
        with open("models_ml/xgb_model.pkl", "rb") as f:
            self.models["xgb"] = pickle.load(f)

    def predict(self, model_name, transaction):
        if model_name not in self.models:
            return {"error": f"Modèle '{model_name}' non chargé."}

        model = self.models[model_name]
        df = pd.DataFrame([transaction])[self.columns].fillna(0)
        pred = model.predict(df)[0]
        proba = model.predict_proba(df)[0][1]
        return {
            "model": model_name,
            "fraud_prediction": int(pred),
            "fraud_probability": float(proba)
        }
