import streamlit as st
import requests
import pandas as pd
from streamlit_pages.anomalies_charts import show_chart, show_table
from streamlit_pages.anomaly_lookup import lookup_transaction

st.set_page_config(page_title="BlockSecure", layout="wide")
st.title("BlockSecure - Analyse des Anomalies")

# Charger les données une fois
try:
    url = "http://127.0.0.1:5000/transactions/anomalies"
    df = pd.DataFrame(requests.get(url).json())

    st.success(f"{len(df)} anomalies chargées")
    show_table(df)
    show_chart(df)
    lookup_transaction()

except Exception as e:
    st.error("Impossible de récupérer les données.")
    st.code(str(e))
