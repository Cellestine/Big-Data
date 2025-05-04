# class AnomalyDetector:
#     def is_anomalous(self, transaction):
#         return transaction.get("FLAG", 0) != 0
        
#     def detect(self, tx):
#         reasons = []

#         if tx.get("Sent tnx", 0) <= 2:
#             reasons.append("Low number of sent transactions (<=2)")

#         balance = tx.get("total ether balance", 0)
#         if balance < 0:
#             reasons.append("Negative ether balance")
#         elif balance > 0.01:
#             reasons.append("Unusually high ether balance (> 0.01)")

#         if tx.get("Number of Created Contracts", 0) > 2:
#             reasons.append("High number of contracts created (>2)")

#         return {
#             "is_anomalous": bool(reasons),
#             "anomaly_reason": reasons
#         }
import numpy as np

class AnomalyDetector:
    def __init__(self, reference_df=None):
        self.df = reference_df  # Pour les règles basées sur statistiques globales

        if self.df is not None:
            # Pré-calculs des seuils statistiques pour éviter de recalculer à chaque transaction
            self.avg_val_sent_threshold = self.df["avg val sent"].quantile(0.99)
            self.erc20_avg_val_sent_mean = self.df["ERC20 avg val sent"].mean()
            self.erc20_avg_val_sent_std = self.df["ERC20 avg val sent"].std()
            self.erc20_avg_val_sent_threshold = self.erc20_avg_val_sent_mean + 3 * self.erc20_avg_val_sent_std

    def detect(self, tx):
        reasons = []

        # 1. Activité faible
        if tx.get("Sent tnx", 0) <= 2:
            reasons.append("Low number of sent transactions (<=2)")

        # 2. Création excessive de contrats
        if tx.get("Number of Created Contracts", 0) > 5:
            reasons.append("High number of created contracts (>5)")

        # 3. Activité flash
        if tx.get("Time Diff between first and last (Mins)", 0) < 5 and tx.get("total transactions (including tnx to create contract", 0) > 5:
            reasons.append("High activity in short time")

        # 4. Ratio envoyées/reçues très déséquilibré
        sent = tx.get("Sent tnx", 1)
        received = tx.get("Received Tnx", 1)
        if sent / max(received, 1) > 10:
            reasons.append("Very high send/receive ratio")

        # 5. Nombre de tokens envoyés très élevé
        if tx.get("ERC20 uniq sent token name", 0) > 10:
            reasons.append("Many different tokens sent (>10)")

        # 6. Valeur moyenne envoyée en ETH anormalement haute (top 1%)
        if self.df is not None:
            if tx.get("avg val sent", 0) > self.avg_val_sent_threshold:
                reasons.append("Unusually high avg ETH sent (top 1%)")

        # 7. Valeur moyenne envoyée ERC20 très déviante (> moyenne + 3σ)
        if self.df is not None:
            if tx.get("ERC20 avg val sent", 0) > self.erc20_avg_val_sent_threshold:
                reasons.append("ERC20 avg sent value very high (outlier)")

        # 8. Large diffusion (nombre de destinataires uniques élevé)
        if tx.get("Unique Sent To Addresses", 0) > 100:
            reasons.append("Very wide token distribution (>100 addresses)")

        # 9. Adresse dormante activée soudainement
        if tx.get("Time Diff between first and last (Mins)", 0) > 10000 and tx.get("total transactions (including tnx to create contract", 0) < 3:
            reasons.append("Long dormancy then sudden activity")


        #------------ ANOMALIES -------------------
                # Solde anormal
        balance = tx.get("total ether balance", 0)
        if balance < 0:
            reasons.append("Negative ether balance")
        elif balance > 1:
            reasons.append("Unusually high ether balance (> 1 ETH)")
        
        return {
            "is_anomalous": bool(reasons),
            "anomaly_reason": reasons
        }


