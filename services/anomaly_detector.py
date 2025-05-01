class AnomalyDetector:
    def is_anomalous(self, transaction):
        return transaction.get("FLAG", 0) != 0
        
    def detect(self, tx):
        reasons = []

        if tx.get("Sent tnx", 0) <= 2:
            reasons.append("Low number of sent transactions (<=2)")

        balance = tx.get("total ether balance", 0)
        if balance < 0:
            reasons.append("Negative ether balance")
        elif balance > 0.01:
            reasons.append("Unusually high ether balance (> 0.01)")

        if tx.get("Number of Created Contracts", 0) > 2:
            reasons.append("High number of contracts created (>2)")

        return {
            "is_anomalous": bool(reasons),
            "anomaly_reason": reasons
        }
