# 📁 streamlit_ml_predict.py
import streamlit as st
import requests

st.set_page_config(page_title="Prédiction ML", layout="wide")

st.title("🧠 Détection de fraude par modèles supervisés")

st.markdown("### 🔍 Tester une transaction spécifique")

tx_id = st.text_input("ID de la transaction (MongoDB)", "")
model = st.selectbox("Modèle ML :", ["xgb", "random_forest", "logistic"])

if st.button("Prédire"):
    if not tx_id:
        st.warning("Merci d’entrer un ID de transaction.")
    else:
        try:
            url = f"http://127.0.0.1:5000/transactions/predict-ml/{tx_id}?model={model}"
            response = requests.get(url)
            if response.status_code == 200:
                result = response.json()
                st.success("✅ Résultat de la prédiction :")
                st.json(result)
            else:
                st.error("❌ Erreur : " + response.text)
        except Exception as e:
            st.error(f"Erreur lors de l’appel à l’API : {e}")
