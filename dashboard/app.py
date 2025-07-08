import sys, os
# ✅ Fix: Add 'src' folder to the Python path so imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import streamlit as st
from core.plot_returns import calculate_returns, summarize_returns, plot_cumulative_returns

st.set_page_config(page_title="FX Sentiment Trading Dashboard", layout="wide")
st.title("📈 FX Sentiment Trading Dashboard")

LOG_FILE = "data/live_signals_log.csv"

# --- 1) Load & enrich all signals ---
try:
    df_full, returns, cumulative = calculate_returns(LOG_FILE)
    if df_full.empty:
        st.warning("⚠️ No valid signals found in log.")
        st.stop()
except Exception as e:
    st.error(f"Error loading performance metrics: {e}")
    st.stop()

# --- 2) Sidebar filters (for attribution & log only) ---
with st.sidebar:
    st.header("🔍 Filters")
    pairs = df_full["pair"].dropna().unique().tolist()
    selected_pairs = st.multiselect("Currency Pairs", pairs, default=pairs)

    sentiments = df_full["label"].dropna().unique().tolist()
    selected_sentiments = st.multiselect("Sentiment", sentiments, default=sentiments)

# apply filters to create a display-subset
df_display = df_full[
    df_full["pair"].isin(selected_pairs) &
    df_full["label"].isin(selected_sentiments)
].copy()

# --- 3) Performance Summary (always on full history) ---
st.subheader("📊 Performance Summary")
metrics = summarize_returns(returns)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Return (%)",   f"{metrics['Total Return']:.2f}")
c2.metric("Sharpe Ratio",       f"{metrics['Sharpe Ratio']:.2f}")
c3.metric("Max Drawdown (%)",   f"{metrics['Max Drawdown']:.2f}")
c4.metric("Win Rate",           f"{metrics['Win Rate'] * 100:.2f}%")

st.pyplot(plot_cumulative_returns(cumulative))

# --- 4) Attribution Analysis (on filtered subset) ---
st.subheader("📌 Attribution Analysis")

st.markdown("**Average Return by Currency Pair**")
pair_stats = df_display.groupby("pair")["return_pct"].mean().sort_values(ascending=False)
st.dataframe(
    pair_stats
      .reset_index()
      .rename(columns={"return_pct":"Avg Return (%)"})
)

st.markdown("**Average Return by Sentiment**")
label_stats = df_display.groupby("label")["return_pct"].mean().sort_values(ascending=False)
st.dataframe(
    label_stats
      .reset_index()
      .rename(columns={"return_pct":"Avg Return (%)"})
)

# --- 5) Live Signals Log (with return_pct & cumulative_return) ---
st.subheader("📄 Live Signals Log")
st.dataframe(
    df_display
      .sort_values("timestamp", ascending=False)
      .reset_index(drop=True)
)
