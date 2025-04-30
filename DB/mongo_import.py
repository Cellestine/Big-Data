import pandas as pd
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Connexion à MongoDB
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db["transactions"]

# Charger le fichier CSV
df = pd.read_csv("fichier/transaction_dataset.csv")

# Convertir le DataFrame en dictionnaires et insérer dans MongoDB
collection.insert_many(df.to_dict(orient="records"))

print("✅ Données insérées dans MongoDB")
