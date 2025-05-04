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

class AnomalyDetector:
    def detect(self, tx):
        reasons = []

        # 1. Activité suspecte
        if tx.get("Sent tnx", 0) <= 2:
            reasons.append("Low number of sent transactions (<=2)")

        # 2. Solde anormal
        balance = tx.get("total ether balance", 0)
        if balance < 0:
            reasons.append("Negative ether balance")
        elif balance > 1:
            reasons.append("Unusually high ether balance (> 1 ETH)")

        # 3. Création excessive de contrats
        if tx.get("Number of Created Contracts", 0) > 5:
            reasons.append("High number of created contracts (>5)")

        # 4. Activité dans un temps très court
        if tx.get("Time Diff between first and last (Mins)", 0) < 5 and tx.get("total transactions (including tnx to create contract", 0) > 5:
            reasons.append("High activity in short time")

        # 5. Ratio tx envoyées / reçues
        sent = tx.get("Sent tnx", 1)
        received = tx.get("Received Tnx", 1)
        if sent / max(received, 1) > 10:
            reasons.append("Very high send/receive ratio")

        # 6. Nombre de tokens différents
        if tx.get("ERC20 uniq sent token name", 0) > 10:
            reasons.append("Many different tokens sent (>10)")

        return {
            "is_anomalous": bool(reasons),
            "anomaly_reason": reasons
        }
