class Transaction:
    @staticmethod
    def to_summary_dict(tx, anomaly_reason):
        return {
            "transaction_id": tx.get("_id"),
            "address": tx.get("Address"),
            "sent_tnx": tx.get("Sent tnx"),
            "ether_balance": tx.get("total ether balance"),
            "contracts_created": tx.get("Number of Created Contracts"),
            "anomaly_reason": anomaly_reason
        }
    
    @staticmethod
    def to_ml_prediction_dict(tx, prediction_result):
        return {
            "transaction_id": tx.get("_id"),
            "address": tx.get("Address"),
            "real_flag": tx.get("FLAG"),
            "model": prediction_result.get("model"),
            "predicted_flag": prediction_result.get("fraud_prediction"),
            "probability": prediction_result.get("fraud_probability")
        }
