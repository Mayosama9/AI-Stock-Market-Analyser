import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
from stock_data import get_latest_stock_info, get_stock_data
from ai_analysis import compare_stocks  # Ensure this function exists

st.set_page_config(page_title="Stock Comparison", layout="wide")
st.title("📊 Compare Two Stocks Side-by-Side")

# 👉 Initialize session state variables (if not set)
if "stock1" not in st.session_state:
    st.session_state.stock1 = ""
if "stock2" not in st.session_state:
    st.session_state.stock2 = ""
if "prev_stock1" not in st.session_state:
    st.session_state.prev_stock1 = ""
if "prev_stock2" not in st.session_state:
    st.session_state.prev_stock2 = ""
if "stock1_info" not in st.session_state:
    st.session_state.stock1_info = None
if "stock2_info" not in st.session_state:
    st.session_state.stock2_info = None
if "comparison_result" not in st.session_state:
    st.session_state.comparison_result = None
if "data1" not in st.session_state:
    st.session_state.data1 = None
if "data2" not in st.session_state:
    st.session_state.data2 = None

# 👉 User Inputs for Two Stocks
col1, col2 = st.columns(2)
with col1:
    stock1_input = st.text_input("Enter First Stock Ticker (e.g., AAPL, TSLA)", value=st.session_state.stock1)
with col2:
    stock2_input = st.text_input("Enter Second Stock Ticker (e.g., MSFT, AMZN)", value=st.session_state.stock2)

# 👉 Reset values if tickers change
if stock1_input != st.session_state.prev_stock1:
    st.session_state.stock1 = stock1_input
    st.session_state.stock1_info = None
    st.session_state.data1 = None
    st.session_state.comparison_result = None
    st.session_state.prev_stock1 = stock1_input  # Update previous stock1 tracker

if stock2_input != st.session_state.prev_stock2:
    st.session_state.stock2 = stock2_input
    st.session_state.stock2_info = None
    st.session_state.data2 = None
    st.session_state.comparison_result = None
    st.session_state.prev_stock2 = stock2_input  # Update previous stock2 tracker

# 👉 User Inputs for Date Range and Interval
st.sidebar.header("📅 Select Date Range & Interval")
start_date = st.sidebar.date_input("Start Date", datetime.date.today() - datetime.timedelta(days=30))
end_date = st.sidebar.date_input("End Date", datetime.date.today())
interval = st.sidebar.selectbox("Select Interval", ["1m", "5m", "15m", "1h", "1d", "5d", "1wk", "1mo", "3mo"], index=4)

# 👉 Fetch stock info only if both tickers are entered
if st.session_state.stock1 and st.session_state.stock2:
    if st.session_state.stock1_info is None:
        st.session_state.stock1_info = get_latest_stock_info(st.session_state.stock1)
    if st.session_state.stock2_info is None:
        st.session_state.stock2_info = get_latest_stock_info(st.session_state.stock2)

    stock1_info = st.session_state.stock1_info
    stock2_info = st.session_state.stock2_info

    if stock1_info and stock2_info:
        # 👉 Display stock data
        st.subheader("📈 Stock Overview")
        col1, col2 = st.columns(2)

        with col1:
            st.metric(f"{stock1_info['name']} ({st.session_state.stock1})", f"${stock1_info['price']}")
            st.write(f"**Market Cap:** ${stock1_info['market_cap']}")
            st.write(f"**Day High:** ${stock1_info['day_high']}")
            st.write(f"**Day Low:** ${stock1_info['day_low']}")
            st.write(f"**Previous Close:** {stock1_info['previous_close']}")

        with col2:
            st.metric(f"{stock2_info['name']} ({st.session_state.stock2})", f"${stock2_info['price']}")
            st.write(f"**Market Cap:** ${stock2_info['market_cap']}")
            st.write(f"**Day High:** ${stock2_info['day_high']}")
            st.write(f"**Day Low:** ${stock2_info['day_low']}")
            st.write(f"**Previous Close:** {stock2_info['previous_close']}")

        # 👉 Fetch stock price history (only if needed)
        if st.session_state.data1 is None:
            st.session_state.data1 = get_stock_data(st.session_state.stock1, start=start_date, end=end_date, interval=interval)
        if st.session_state.data2 is None:
            st.session_state.data2 = get_stock_data(st.session_state.stock2, start=start_date, end=end_date, interval=interval)

        data1 = st.session_state.data1
        data2 = st.session_state.data2

        if data1 is not None and not data1.empty and data2 is not None and not data2.empty:
            # 👉 Plot Stock Prices
            st.subheader(f"📉 Stock Price Comparison ({interval} Interval)")
            fig = px.line()
            fig.add_scatter(x=data1.index, y=data1["Close"], mode="lines", name=f"{st.session_state.stock1} Price")
            fig.add_scatter(x=data2.index, y=data2["Close"], mode="lines", name=f"{st.session_state.stock2} Price")
            fig.update_layout(title="Stock Price Comparison", xaxis_title="Date", yaxis_title="Closing Price")
            st.plotly_chart(fig)

        # 👉 AI-Powered Insights for Comparison (fetch only once)
        st.subheader("🧠 AI-Powered Stock Comparison")
        if st.session_state.comparison_result is None:
            with st.spinner("Analyzing stocks..."):
                st.session_state.comparison_result = compare_stocks(st.session_state.stock1, st.session_state.stock2)

        st.markdown(st.session_state.comparison_result)

    else:
        st.error("❌ One or both stock tickers are invalid. Please check the ticker symbols.")


