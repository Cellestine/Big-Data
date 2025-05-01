class AnomalyDetector:
    def is_anomalous(self, transaction):
        return transaction.get("FLAG", 0) != 0
        
