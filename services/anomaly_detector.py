class AnomalyDetector:
    def __init__(self, threshold=10000):
        self.threshold = threshold

    def is_anomalous(self, transaction):
        amount = transaction.get("amount", 0)
        return amount > self.threshold
