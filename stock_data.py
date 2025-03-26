import yfinance as yf
import pandas as pd
import requests
from config import *

def get_stock_data(ticker, start=None, end=None, interval="1d", prepost=False, auto_adjust=True, actions=True):
    """
    Fetch historical stock data with customizable parameters.
    """
    stock = yf.Ticker(ticker)
    data = stock.history(
        start=start, 
        end=end, 
        interval=interval, 
        prepost=prepost, 
        auto_adjust=auto_adjust, 
        actions=actions
    )
    return data

def get_latest_stock_info(ticker):
    """Fetch latest stock price and market summary."""
    stock = yf.Ticker(ticker)
    info = stock.info
    
    return {
        "name": info.get("longName", "N/A"),
        "price": info.get("regularMarketPrice", "N/A"),
        "market_cap": info.get("marketCap", "N/A"),
        "previous_close": info.get("previousClose", "N/A"),
        "day_high": info.get("dayHigh", "N/A"),
        "day_low": info.get("dayLow", "N/A")
    }

def get_financial_statements(ticker):
    """Fetch balance sheet, income statement, and cash flow data."""
    stock = yf.Ticker(ticker)

    financials = {
        "income_statement": stock.financials.T,  # Transpose for better readability
        "balance_sheet": stock.balance_sheet.T,
        "cash_flow": stock.cashflow.T
    }
    
    return financials