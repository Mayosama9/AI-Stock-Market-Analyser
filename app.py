import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
from stock_data import get_stock_data, get_latest_stock_info
from ai_analysis import analyze_stock_trends

st.set_page_config(page_title="AI Stock Market Insights", layout="wide")

st.title("📈 AI-Powered Real-Time Stock Market Insights")

# 👉 Initialize session state variables
if "ticker" not in st.session_state:
    st.session_state.ticker = ""
if "start_date" not in st.session_state:
    st.session_state.start_date = datetime.date.today() - datetime.timedelta(days=30)
if "end_date" not in st.session_state:
    st.session_state.end_date = datetime.date.today()
if "interval" not in st.session_state:
    st.session_state.interval = "1d"
if "prepost" not in st.session_state:
    st.session_state.prepost = False
if "auto_adjust" not in st.session_state:
    st.session_state.auto_adjust = True
if "actions" not in st.session_state:
    st.session_state.actions = True
if "stock_info" not in st.session_state:
    st.session_state.stock_info = None
if "stock_data" not in st.session_state:
    st.session_state.stock_data = None
if "ai_summary" not in st.session_state:
    st.session_state.ai_summary = None

# 👉 User Inputs (with session state)
st.session_state.ticker = st.text_input(
    "Enter Stock Ticker (e.g., AAPL, TSLA, MSFT):", value=st.session_state.ticker
)

col1, col2 = st.columns(2)
with col1:
    st.session_state.start_date = st.date_input("Start Date", value=st.session_state.start_date)
with col2:
    st.session_state.end_date = st.date_input("End Date", value=st.session_state.end_date)

# Additional parameters
st.session_state.interval = st.selectbox(
    "Interval", ["1m", "5m", "15m", "1h", "1d", "5d", "1wk", "1mo"], 
    index=["1m", "5m", "15m", "1h", "1d", "5d", "1wk", "1mo"].index(st.session_state.interval)
)
st.session_state.prepost = st.checkbox("Include Pre/Post Market Data", value=st.session_state.prepost)
st.session_state.auto_adjust = st.checkbox("Auto Adjust Prices", value=st.session_state.auto_adjust)
st.session_state.actions = st.checkbox("Include Stock Splits & Dividends", value=st.session_state.actions)

# 👉 Fetch stock data only if ticker is entered
if st.session_state.ticker:
    if st.session_state.stock_info is None or st.session_state.ticker != st.session_state.stock_info.get("symbol"):
        st.session_state.stock_info = get_latest_stock_info(st.session_state.ticker)

    stock_info = st.session_state.stock_info

    if stock_info:
        st.subheader(f"📊 {stock_info['name']} Stock Summary")
        st.metric("Current Price", f"${stock_info['price']}")
        st.metric("Market Cap", f"${stock_info['market_cap']}")
        st.metric("Day High", f"${stock_info['day_high']}")
        st.metric("Day Low", f"${stock_info['day_low']}")

        # 👉 Fetch stock historical data
        if st.session_state.stock_data is None or st.session_state.ticker != stock_info.get("symbol"):
            st.session_state.stock_data = get_stock_data(
                st.session_state.ticker, 
                start=st.session_state.start_date, 
                end=st.session_state.end_date, 
                interval=st.session_state.interval, 
                prepost=st.session_state.prepost, 
                auto_adjust=st.session_state.auto_adjust, 
                actions=st.session_state.actions
            )

        data = st.session_state.stock_data

        if data is not None and not data.empty:
            st.subheader(f"📉 Stock Price Trend ({st.session_state.start_date} to {st.session_state.end_date})")
            fig = px.line(data, x=data.index, y="Close", title="Stock Price Trend")
            st.plotly_chart(fig)

            # 👉 AI-Powered Market Analysis
            st.subheader("🧠 AI-Powered Market Analysis")
            with st.spinner("Generating insights..."):
                if st.session_state.ai_summary is None or st.session_state.ticker != stock_info.get("symbol"):
                    st.session_state.ai_summary = analyze_stock_trends(st.session_state.ticker, data.to_dict())

                st.markdown(st.session_state.ai_summary)

        else:
            st.warning("No historical data available for this stock in the given date range.")
    else:
        st.error("Stock data not found. Please check the ticker.")

# 👉 Navigation Buttons for Other Pages (data is now preserved across pages)
col1, col2 = st.columns(2)
with col1:
    if st.button("🔄 Compare Stocks"):
        st.session_state.page = "compare_stocks"
        st.switch_page("pages/compare_stocks.py")
with col2:
    if st.button("💬 AI Chat Assistant"):
        st.session_state.page = "chat"
        st.switch_page("pages/chat.py")
