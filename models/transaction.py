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
