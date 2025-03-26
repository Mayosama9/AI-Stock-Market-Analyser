import requests
import json
import yfinance as yf
from stock_data import get_latest_stock_info
from config import OPENAI_API_KEY, OPENAI_API_BASE, MODEL_NAME

def analyze_stock_trends(ticker, stock_summary):
    """Generate AI-powered financial trend analysis using an API request."""

    url = f"{OPENAI_API_BASE}"  # Adjust if using a different API

    headers = {
        "api-key": OPENAI_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "You are an AI financial analyst."},
            {"role": "user", "content": f"""Based on the following stock data: 
                {stock_summary}

                Provide an analysis on current trends, potential risks, and investment suggestions for {ticker}.
                """}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raises an error for 4XX/5XX responses
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Example usage
# result = analyze_stock_trends("AAPL", "Stock is up 5% today...")
# print(result)

 


def compare_stocks(ticker1, ticker2):
    """Fetches stock data and uses AI to compare two stocks."""

    stock1 = get_latest_stock_info(ticker1)
    stock2 = get_latest_stock_info(ticker2)

    if not stock1 or not stock2:
        return "Error: One or both stock tickers are invalid."

    # Use AI to analyze and compare
    url = OPENAI_API_BASE  # Adjust if using a different API

    headers = {
        "api-key": OPENAI_API_KEY,
        "Content-Type": "application/json"
    }

    # Structure input for AI
    stock_data = f"""
    Compare the following two stocks based on financial data:

    **Stock 1:** {stock1['name']} ({ticker1})
    - Current Price: ${stock1['price']}
    - Market Cap: ${stock1['market_cap']}
    - Day High: ${stock1['day_high']}
    - Day Low: ${stock1['day_low']}
    - P/E Ratio: {stock1.get('trailingPE', 'N/A')}
    - Volume: {stock1.get('volume', 'N/A')}

    **Stock 2:** {stock2['name']} ({ticker2})
    - Current Price: ${stock2['price']}
    - Market Cap: ${stock2['market_cap']}
    - Day High: ${stock2['day_high']}
    - Day Low: ${stock2['day_low']}
    - P/E Ratio: {stock2.get('trailingPE', 'N/A')}
    - Volume: {stock2.get('volume', 'N/A')}

    Analyze and determine:
    - Which stock is currently performing better?
    - Which stock has better growth potential?
    - Any risks or concerns?
    - If an investor had to choose, which would be a better buy and why?
    """

    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "You are an AI financial analyst."},
            {"role": "user", "content": stock_data}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raises an error for 4XX/5XX responses
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

    
