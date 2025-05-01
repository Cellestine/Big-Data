import streamlit as st
import pandas as pd

def show_table(df):
    st.subheader("Transactions Anormales")
    st.dataframe(df[["_id", "Address", "total ether balance", "Sent tnx", "anomaly_reason"]])


def show_chart(df):
    st.subheader("Raisons des anomalies")
    exploded = df.explode("anomaly_reason")
    count = exploded["anomaly_reason"].value_counts().reset_index()
    count.columns = ["Raison", "Nombre"]
    st.bar_chart(count.set_index("Raison"))

