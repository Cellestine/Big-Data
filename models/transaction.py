class Transaction:
    def __init__(self, from_address, to_address, amount, timestamp, **kwargs):
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.timestamp = timestamp
        self.extra_data = kwargs

    def to_dict(self):
        data = {
            "from_address": self.from_address,
            "to_address": self.to_address,
            "amount": self.amount,
            "timestamp": self.timestamp
        }
        data.update(self.extra_data)  # Ajouter d'autres champs si besoin
        return data
