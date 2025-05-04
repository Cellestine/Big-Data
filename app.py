from flask import Flask, request, render_template
from dotenv import load_dotenv
from flask_restx import Api, Resource
import os
from DB.database import MongoDB
from models.transaction import Transaction
from services.anomaly_detector import AnomalyDetector
from services.ml_detector import MLAnomalyDetector
from services.supervised_models import MultiModelFraudDetector

# Initialisation Flask + RESTX
app = Flask(__name__)
api = Api(app, title="BlockSecure API", version="1.0", description="Détection d'anomalies sur les transactions Ethereum")
ns = api.namespace("transactions", description="Opérations sur les transactions")

# Chargement variables d'env
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Initialisation MongoDB + Anomalie
db = MongoDB(uri=MONGO_URI, db_name=DATABASE_NAME)
anomaly_detector = AnomalyDetector()



@ns.route("/<string:transaction_id>")
class TransactionItem(Resource):
    def get(self, transaction_id):
        tx = db.get_transaction_by_id(transaction_id)
        if not tx:
            return {"error": "Transaction non trouvée"}, 404
        tx["_id"] = str(tx["_id"])
        tx["is_anomalous"] = anomaly_detector.is_anomalous(tx)
        return tx


@ns.route("/anomalies")
class AnomalyList(Resource):
    def get(self):
        transactions = db.get_all_transactions()
        anomalies = []

        for tx in transactions:
            tx["_id"] = str(tx["_id"])
            result = anomaly_detector.detect(tx)

            if result["is_anomalous"]:
                tx.update(result)
                anomalies.append(tx)

        return anomalies


@ns.route("/anomalies/<string:transaction_id>")
class AnomalyDetails(Resource):
    def get(self, transaction_id):
        tx = db.get_transaction_by_id(transaction_id)
        if not tx:
            return {"error": "Transaction non trouvée"}, 404

        tx["_id"] = str(tx["_id"])
        result = anomaly_detector.detect(tx)

        if not result["is_anomalous"]:
            return {
                "message": "Cette transaction n’est pas considérée comme anormale.",
                "transaction_id": tx["_id"]
            }

        # Retourner un résumé clair de la transaction
        return Transaction.to_summary_dict(tx, result["anomaly_reason"])

# # entraînement dès le démarrage non supervisé
# ml_detector = MLAnomalyDetector()
# ml_detector.fit(db.get_all_transactions())  # entraînement au lancement

ml_detector = MultiModelFraudDetector()
ml_detector.load_models()

@ns.route("/predict-ml/<string:transaction_id>")
class PredictML(Resource):
    def get(self, transaction_id):
        model_name = request.args.get("model", "xgb")

        # Récupérer la transaction
        transaction = db.get_transaction_by_id(transaction_id)
        if not transaction:
            return {"error": "Transaction introuvable"}, 404

        transaction["_id"] = str(transaction["_id"])
        prediction_result = ml_detector.predict(model_name, transaction)

        if "error" in prediction_result:
            return prediction_result, 400

        summary = Transaction.to_ml_prediction_dict(transaction, prediction_result)
        return summary


if __name__ == "__main__":
    app.run(debug=True)
