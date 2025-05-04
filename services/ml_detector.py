import pandas as pd
from sklearn.ensemble import IsolationForest

class MLAnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.02, random_state=42)
        self.fitted = False
        self.features = [
            "Sent tnx", "Received Tnx", "total ether balance",
            "total ether sent", "avg val sent", "avg val received"
        ]

    def fit(self, data: list):
        df = pd.DataFrame(data)
        df_features = df[self.features].fillna(0)
        self.model.fit(df_features)
        self.fitted = True

    def predict(self, transaction):
        if not self.fitted:
            return False, None

        df_tx = pd.DataFrame([transaction])
        df_tx = df_tx[self.features].fillna(0)

        pred = self.model.predict(df_tx)[0]
        score = self.model.decision_function(df_tx)[0]
        return pred == -1, score
