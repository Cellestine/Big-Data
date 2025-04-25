from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from database import MongoDB
from models.transaction import Transaction
from services.anomaly_detector import AnomalyDetector

# Charger d'abord les variables d'environnement
load_dotenv()

# Ensuite récupérer les variables
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
SECRET_KEY = os.getenv("SECRET_KEY")

# Maintenant on peut initialiser Flask et Mongo
app = Flask(__name__)
db = MongoDB(uri=MONGO_URI, db_name=DATABASE_NAME)  # <-- ici il faut passer uri et db_name !!
anomaly_detector = AnomalyDetector()

# Maintenant tes routes Flask
@app.route("/transactions", methods=["POST"])
def add_transaction():
    data = request.json
    tx = Transaction(
        from_address=data.get("from_address"),
        to_address=data.get("to_address"),
        amount=data.get("amount"),
        timestamp=data.get("timestamp")
    )
    transaction_id = db.insert_transaction(tx.to_dict())
    return jsonify({"message": "Transaction ajoutée", "id": str(transaction_id)}), 201

@app.route("/transactions", methods=["GET"])
def list_transactions():
    transactions = db.get_all_transactions()
    formatted = []
    for tx in transactions:
        tx["_id"] = str(tx["_id"])
        tx["is_anomalous"] = anomaly_detector.is_anomalous(tx)
        formatted.append(tx)
    return jsonify(formatted)

@app.route("/transactions/<transaction_id>", methods=["GET"])
def get_transaction(transaction_id):
    tx = db.get_transaction_by_id(transaction_id)
    if not tx:
        return jsonify({"error": "Transaction non trouvée"}), 404
    tx["_id"] = str(tx["_id"])
    tx["is_anomalous"] = anomaly_detector.is_anomalous(tx)
    return jsonify(tx)

if __name__ == "__main__":
    app.run(debug=True)
