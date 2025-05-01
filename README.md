# BlockSecure — Détection d'Anomalies sur la Blockchain Ethereum

BlockSecure est une API web et un tableau de bord interactif permettant de détecter automatiquement des anomalies dans les transactions Ethereum.  
Le projet repose sur une architecture **Flask + MongoDB + Streamlit**, avec analyse statistique et visualisation.

---

## Structure du projet


---

## Prérequis

- Python 3.9+
- pip
- MongoDB en local ou distant

---

## Installation

1. **Clone du projet**
```bash
git clone https://github.com/Cellestine/Big-Data.git
cd BlockSecure
```

2. **Création de l’environnement**
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. **Installation des dépendances**
```bash
pip install -r requirements.txt
```

4. **Configuration des variables .env Crée un fichier .env à la racine**
```ini
MONGO_URI=mongodb://localhost:27017/
DATABASE_NAME=blocksecure
```

---
## Lancer l'API Flask
---

```bash
python app.py
```

---
## Dashboard interactif (Streamlit)
---

Lance le tableau de bord visuel :
```bash
streamlit run streamlit_dashboard.py
```
Fonctionnalités :

- Liste des anomalies
- Graphique des causes (bar chart)
- Recherche de transaction par ID


---
## Détection d’anomalies
---

La détection est basée sur des règles simples :

- Sent tnx <= 2 ➜ activité très faible
- Balance < 0 ou > 0.01 ➜ solde incohérent
- Contracts created > 2 ➜ comportement inhabituel

Chaque transaction suspecte est annotée avec une ou plusieurs raisons (anomaly_reason).
