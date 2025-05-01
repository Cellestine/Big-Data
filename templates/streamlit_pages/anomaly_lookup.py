import streamlit as st
import requests

def lookup_transaction():
    st.subheader("Rechercher une transaction par ID")
    transaction_id = st.text_input("Entrez l'ID :")

    if transaction_id:
        try:
            url = f"http://127.0.0.1:5000/transactions/anomalies/{transaction_id}"
            res = requests.get(url)
            if res.status_code == 200:
                st.json(res.json())
            else:
                st.warning("Aucune anomalie trouvée pour cet ID.")
        except Exception as e:
            st.error("Erreur lors de la requête :")
            st.code(str(e))
