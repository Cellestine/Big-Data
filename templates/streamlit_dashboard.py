import streamlit as st
import requests
import pandas as pd
from streamlit_pages.anomalies_charts import show_table,show_chart,show_correlation_heatmap,show_balance_vs_activity,show_top_tokens_sent,show_ether_kpis
from streamlit_pages.anomaly_lookup import lookup_transaction


# Configuration de la page Streamlit (titre, largeur)
st.set_page_config(page_title="BlockSecure", layout="wide")
st.title("🛡️ BlockSecure - Analyse des Anomalies")

# Tentative de récupération des données d'anomalies depuis l'API Flask locale
try:
    url = "http://127.0.0.1:5000/transactions/anomalies"
    df = pd.DataFrame(requests.get(url).json())
    df.columns = df.columns.str.strip()  # Supprime les espaces avant/après les noms

    url_all = "http://127.0.0.1:5000/transactions/all"
    df_all = pd.DataFrame(requests.get(url_all).json())
    df_all.columns = df_all.columns.str.strip()


    st.markdown(" 📌 Indicateurs Clés")
    st.write("Colonnes disponibles :", df_all.columns.tolist())


    # ------- Affichage des KPIS -----------------
    col1, col2, col3, col4 = st.columns(4)

    df_flagged = df_all[df_all["FLAG"] == 1]  # Anomalies réelles
    with col1:
        st.metric(label="📊 Transactions Totales", value=len(df_all))

    with col2:
        nb_anomalies = len(df_flagged)
        pct_anomalies = (nb_anomalies / len(df_all) * 100) if len(df_all) > 0 else 0

        st.metric(
            label="🚨 Anomalies",
            value=f"{pct_anomalies:.2f}%",
            delta=f"{nb_anomalies} sur {len(df_all)}",
            delta_color="inverse"
        )
    
    if "total Ether sent" in df_all.columns and "total ether received" in df_all.columns:
        #KPI 3 : Volume total Echangé
        total_sent = df_all["total Ether sent"].abs().sum()
        total_received = df_all["total ether received"].sum()
        total_volume = total_sent + total_received
        with col3:
            st.metric("💰 Volume Total (ETH)", f"{total_volume:,.2f} ETH")

        # KPI 4 : Volume suspect échangé
        anomaly_sent = df_flagged["total Ether sent"].abs().sum()
        anomaly_received = df_flagged["total ether received"].sum()
        anomaly_volume = anomaly_sent + anomaly_received
        pct_anomaly_vol = (anomaly_volume / total_volume * 100) if total_volume > 0 else 0
        with col4:
            st.metric("⚠️ Volume Suspect", f"{anomaly_volume:,.2f} ETH", f"{pct_anomaly_vol:.2f}%")   


    #------------------------------------------------------------#
    # Création de trois onglets pour structurer l'application
    tab1, tab2, tab3 = st.tabs([
        "📊 Analyse",
        "📋 Raws",
        "🔎 Recherche"
    ])

    # Onglet 1 : Visualisations graphiques et indicateurs
    with tab1:
        show_ether_kpis(df)  # Indicateurs clés sur les anomalies
        st.subheader("Analyse Graphique des Anomalies")
        show_chart(df)  # Graphique des raisons d’anomalies

        st.divider()  # Séparateur visuel

        # # Indicateurs complémentaires
        # colgraph1, colgraph2 = st.columns(2)
        # with colgraph1:
        #     st.subheader("📈 Activité vs Solde")
        #     show_balance_vs_activity(df) # Scatter plot balance vs activité
        # with colgraph2:
        #     st.subheader("📊 Corrélations entre Variables")
        #     show_correlation_heatmap(df) # Corrélations entre variables
        
        show_top_tokens_sent(df)         # Tokens les plus envoyés

    # Onglet 2 : Tableau de données brutes
    with tab2:
        st.subheader("Tableau des Transactions Anormales")
        show_table(df)  # Affichage des anomalies sous forme de tableau

    # Onglet 3 : Moteur de recherche d'une adresse / transaction spécifique
    with tab3:
        st.subheader("Recherche par Adresse / Transaction")
        lookup_transaction()

# En cas d'échec de connexion à l'API, afficher une erreur lisible
except Exception as e:
    st.error("❌ Impossible de récupérer les données.")
    st.code(str(e))
