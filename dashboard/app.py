import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="FX Sentiment Trading Bot", layout="wide")

st.title("💹 FX Sentiment Trading Bot Dashboard")

# Load signals
df = pd.read_csv("data/live_signals_log.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Sidebar filters
st.sidebar.header("Filters")
currency_filter = st.sidebar.multiselect(
    "Currency Pair", options=df["pair"].unique(), default=df["pair"].unique()
)
sentiment_filter = st.sidebar.multiselect(
    "Sentiment", options=df["label"].unique(), default=df["label"].unique()
)

# Apply filters
filtered_df = df[df["pair"].isin(currency_filter)]
filtered_df = filtered_df[filtered_df["label"].isin(sentiment_filter)]

# Show data
st.subheader("📄 Logged Trade Signals")
st.dataframe(filtered_df.sort_values(by="timestamp", ascending=False), use_container_width=True)

# Chart 1: Sentiment counts by currency pair
st.subheader("📊 Sentiment Distribution by Pair")
sentiment_chart = px.histogram(
    filtered_df,
    x="pair",
    color="label",
    barmode="group",
    title="Sentiment Count per FX Pair",
    labels={"label": "Sentiment"},
)
st.plotly_chart(sentiment_chart, use_container_width=True)

# Chart 2: Signal volume over time
st.subheader("⏱ Signal Volume Over Time")
time_chart = px.histogram(
    filtered_df,
    x="timestamp",
    color="pair",
    nbins=30,
    title="Signal Frequency Over Time",
)
st.plotly_chart(time_chart, use_container_width=True)
