import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from pattern_detector import detect_patterns
from backtester import backtest_patterns
from notifier import send_telegram_message
import time

# Streamlit page configuration
st.set_page_config(page_title="Real-Time Chart Pattern Detector", layout="wide")

# Title and description
st.title("📈 Real-Time Chart Pattern Detection Tool")
st.markdown("""
This tool detects chart patterns in real-time stock data, provides visual alerts, 
Telegram notifications, and backtesting results.
""")

# Sidebar for user inputs
st.sidebar.header("Configuration")
ticker = st.sidebar.text_input("Stock Ticker (e.g., AAPL, TSLA)", value="AAPL")
interval = st.sidebar.selectbox("Data Interval", ["1m", "5m", "15m", "1h", "1d"], index=2)
period = st.sidebar.selectbox("Data Period", ["1d", "5d", "1mo", "3mo", "6mo"], index=1)

# Telegram configuration (hardcoded)
TELEGRAM_BOT_TOKEN = "7424007039:AAG62YomUNo2ipomDJsUk-nlDCDEiky6IS0"
TELEGRAM_CHAT_ID = "charts_pattern_bot"

# Fetch real-time stock data
@st.cache_data(ttl=60)
def fetch_data(ticker, period, interval):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period, interval=interval)
    return data

# Main app logic
if ticker:
    try:
        # Fetch data
        data = fetch_data(ticker, period, interval)
        if data.empty:
            st.error("No data fetched. Please check the ticker or try again later.")
        else:
            st.subheader(f"Stock Data for {ticker}")
            st.dataframe(data.tail())

            # Detect patterns
            patterns = detect_patterns(data)
            
            # Plot chart with patterns
            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name="OHLC"
            ))
            
            # Add pattern annotations
            for pattern, info in patterns.items():
                if info['detected']:
                    for idx in info['points']:
                        fig.add_vline(x=data.index[idx], line_dash="dash", line_color="red")
                    st.success(f"**{pattern}** detected! Suggested Action: {info['action']}")
                    
                    # Send Telegram notification
                    message = f"{pattern} detected for {ticker} at {data.index[-1]}! Action: {info['action']}"
                    try:
                        send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)
                        st.info("Telegram notification sent")
                    except Exception as e:
                        st.warning(f"Failed to send Telegram notification: {str(e)}")

            fig.update_layout(
                title=f"{ticker} Stock Chart with Pattern Detection",
                xaxis_title="Date",
                yaxis_title="Price",
                xaxis_rangeslider_visible=False
            )
            st.plotly_chart(fig, use_container_width=True)

            # Backtesting section
            st.subheader("Backtesting Results")
            if st.button("Run Backtest"):
                backtest_results = backtest_patterns(data, patterns)
                for pattern, stats in backtest_results.items():
                    st.write(f"**{pattern}**")
                    st.write(f"Occurrences: {stats['count']}")
                    st.write(f"Success Rate: {stats['success_rate']:.2%}")
                    st.write(f"Average Return: {stats['avg_return']:.2%}")

    except Exception as e:
        st.error(f"Error: {str(e)}")

# Real-time update loop
if st.sidebar.checkbox("Enable Real-Time Updates", value=False):
    placeholder = st.empty()
    while True:
        data = fetch_data(ticker, period, interval)
        placeholder.dataframe(data.tail())
        time.sleep(60)  # Update every minute