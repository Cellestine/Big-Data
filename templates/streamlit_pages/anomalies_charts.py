# import streamlit as st
# import pandas as pd

# def show_table(df):
#     st.subheader("Transactions Anormales")
#     st.dataframe(df[["_id", "Address", "total ether balance", "Sent tnx", "anomaly_reason"]])


# def show_chart(df):
#     st.subheader("Raisons des anomalies")
#     exploded = df.explode("anomaly_reason")
#     count = exploded["anomaly_reason"].value_counts().reset_index()
#     count.columns = ["Raison", "Nombre"]
#     st.bar_chart(count.set_index("Raison"))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Appliquer un style sobre
sns.set_theme(style="whitegrid")

sns.set_palette("Blues")

# ➤ 1. Tableau principal
def show_table(df):
    st.subheader("📋 Transactions Anormales")
    st.dataframe(df[["_id", "Address", "total ether balance", "Sent tnx", "anomaly_reason"]])

# ➤ 2. Histogramme des raisons d'anomalies
def show_chart(df):
    st.subheader("📊 Raisons des Anomalies")
    exploded = df.explode("anomaly_reason")
    count = exploded["anomaly_reason"].value_counts().reset_index()
    count.columns = ["Raison", "Nombre"]
    st.bar_chart(count.set_index("Raison"))

# ➤ 3. Heatmap des corrélations
def show_correlation_heatmap(df):
    st.subheader("🔍 Corrélation entre les Variables")
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.shape[1] < 2:
        st.warning("Pas assez de données numériques pour afficher une heatmap.")
        return
    corr = numeric_df.corr()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr, cmap="Blues", annot=False, ax=ax)
    st.pyplot(fig)

# ➤ 4. Scatter Plot : activité vs solde
def show_balance_vs_activity(df):
    st.subheader("📈 Solde Ether vs Transactions Envoyées")
    if "Sent tnx" not in df or "total ether balance" not in df:
        st.warning("Colonnes manquantes pour le graphique.")
        return

    fig, ax = plt.subplots()
    ax.scatter(df["Sent tnx"], df["total ether balance"], alpha=0.6, color="#4A90E2")
    ax.set_xlabel("Transactions envoyées")
    ax.set_ylabel("Solde total (ETH)")
    st.pyplot(fig)

# ➤ 5. Top tokens envoyés
def show_top_tokens_sent(df):
    st.subheader("🏷️ Top Tokens Envoyés (ERC20)")
    if "ERC20 most sent token type" in df:
        top_tokens = df["ERC20 most sent token type"].value_counts().head(10)
        st.bar_chart(top_tokens)
    else:
        st.info("Aucune donnée de token envoyée disponible.")


# ➤ 6. KPI Ether
def show_ether_kpis(df):
    anomalous_df = df[df["anomaly_reason"].notna()]

    if "total ether received" in df.columns and "total ether sent" in df.columns:
        total_sent = df["total ether sent"].abs().sum()
        total_received = df["total ether received"].sum()
        total_volume = total_sent + total_received

        anomaly_sent = anomalous_df["total ether sent"].abs().sum()
        anomaly_received = anomalous_df["total ether received"].sum()
        anomaly_volume = anomaly_sent + anomaly_received

        pct_anomaly_volume = (anomaly_volume / total_volume * 100) if total_volume > 0 else 0

        col7, col8 = st.columns(2)
        with col7:
            st.metric("💰 Ether Total Échangé", f"{total_volume:,.2f} ETH")
        with col8:
            st.metric("🚨 Ether Échangé Suspect", f"{anomaly_volume:,.2f} ETH", f"{pct_anomaly_volume:.2f}%")
