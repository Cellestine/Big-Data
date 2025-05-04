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

    ALL_REASONS = [
        "Low number of sent transactions (<=2)",
        "High number of created contracts (>5)",
        "High activity in short time",
        "Very high send/receive ratio",
        "Many different tokens sent (>10)",
        "Unusually high avg ETH sent (top 1%)",
        "ERC20 avg sent value very high (outlier)",
        "Very wide token distribution (>100 addresses)",
        "Long dormancy then sudden activity",
        "Negative ether balance",
        "Unusually high ether balance (> 1 ETH)"
    ]

    exploded = df.explode("anomaly_reason")
    count = exploded["anomaly_reason"].value_counts().reindex(ALL_REASONS, fill_value=0)
    count = count.reset_index()
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

def show_top_tokens_sent(df):
    st.subheader("🏷️ Top Tokens Envoyés (ERC20)")

    column = "ERC20 most sent token type"
    
    if column in df:
        # Nettoyage : on enlève les NaN, les "0", les chaînes vides et les espaces
        cleaned_series = df[column].dropna()
        cleaned_series = cleaned_series[cleaned_series.astype(str).str.strip().ne("0")]
        cleaned_series = cleaned_series[cleaned_series.astype(str).str.strip().ne("")]

        if cleaned_series.empty:
            st.info("Aucun token pertinent envoyé dans les données.")
        else:
            top_tokens_df = cleaned_series.value_counts().head(10).reset_index()
            top_tokens_df.columns = ["Token", "Count"]
            top_tokens_df = top_tokens_df.set_index("Token")  # pour que les labels restent en ordre
            st.bar_chart(top_tokens_df)

    else:
        st.info("Colonne non disponible dans les données.")



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
