import pandas as pd
import streamlit as st
import os
from datetime import datetime

LOG_FILE = "data/live_signals_log.csv"

st.set_page_config(page_title="FX Sentiment Trading Dashboard", layout="wide")

st.title("💹 FX Sentiment Trading Dashboard")
st.markdown("Real-time sentiment predictions and trading signals.")

# Load data
if not os.path.exists(LOG_FILE):
    st.warning("No signals logged yet.")
    st.stop()

df = pd.read_csv(LOG_FILE)

# Filters
pairs = df["pair"].unique().tolist()
selected_pairs = st.multiselect("Select Currency Pairs", pairs, default=pairs)

labels = df["label"].unique().tolist()
selected_labels = st.multiselect("Select Sentiment", labels, default=labels)

df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df[df["pair"].isin(selected_pairs) & df["label"].isin(selected_labels)]

# Display Table
st.subheader("📋 Latest Signals")
st.dataframe(df.sort_values("timestamp", ascending=False), use_container_width=True)

# Summary
st.subheader("📈 Signal Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Signals", len(df))
col2.metric("Positive", (df["label"] == "positive").sum())
col3.metric("Negative", (df["label"] == "negative").sum())

# Auto-refresh
st.markdown("🔁 Refresh this page to get the latest updates.")
