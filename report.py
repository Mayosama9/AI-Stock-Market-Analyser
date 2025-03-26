import streamlit as st
import pandas as pd
from stock_data import *

# Streamlit Page Configuration
st.set_page_config(page_title="Stock Financial Report", layout="wide")

# Sidebar for User Input
st.sidebar.header("Financial Report Generator")
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, TSLA):", "AAPL")

if ticker:
    # Fetch Stock Information
    stock_info = get_latest_stock_info(ticker)
    financials = get_financial_statements(ticker)

    if stock_info and financials:
        st.title(f"📊 Financial Report for {stock_info['name']} ({ticker})")

        # Display Key Stock Metrics
        st.metric(label="Current Price", value=f"${stock_info['price']}")
        st.metric(label="Market Cap", value=f"${stock_info['market_cap']:,}")
        st.metric(label="Previous Close", value=f"${stock_info['previous_close']}")

        # Display Financial Statements
        st.subheader("📄 Income Statement (Yearly)")
        st.dataframe(financials["income_statement"])

        st.subheader("📄 Balance Sheet (Yearly)")
        st.dataframe(financials["balance_sheet"])

        st.subheader("📄 Cash Flow Statement (Yearly)")
        st.dataframe(financials["cash_flow"])

        # Generate AI Financial Analysis
        


    else:
        st.error("❌ Unable to fetch financial data. Please try a different ticker.")
