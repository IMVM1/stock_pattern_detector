import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pattern_detector import detect_patterns, get_pattern_description
from backtester import backtest_patterns
from data_fetcher import fetch_alpha_vantage_data
import time
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Streamlit page configuration
st.set_page_config(page_title="Real-Time Chart Pattern Detector", layout="wide")

# Title and description
st.title("📈 Advanced Chart Pattern Detection Tool")
st.markdown("""
This tool detects chart patterns in real-time stock data using Alpha Vantage, provides visual alerts with suggested actions, 
technical indicators, historical pattern comparisons, and backtesting with exportable results.
""")

# Ticker suggestions
TICKER_SUGGESTIONS = ["AAPL", "TSLA", "MSFT", "RELIANCE.NS", "INFY.NS", "TCS.NS"]

# Sidebar for user inputs
st.sidebar.header("Configuration")
ticker = st.sidebar.selectbox("Stock Ticker (e.g., AAPL, RELIANCE.NS)", options=TICKER_SUGGESTIONS + [""], format_func=lambda x: x if x else "Enter custom ticker")
custom_ticker = st.sidebar.text_input("Custom Ticker (if not in list)", value="")
ticker = custom_ticker if custom_ticker else ticker

# Alpha Vantage API key (hardcoded for testing)
ALPHA_VANTAGE_KEY = "P1HAF0HQIWQJLUHM"

# Restrict intervals based on period
period = st.sidebar.selectbox("Data Period", ["1d", "5d", "1mo", "3mo", "6mo"], index=1, key="period_select")
if period in ["1d", "5d"]:
    interval_options = ["1m", "5m", "15m", "1h", "1d"]
    default_interval = "1m" if period == "1d" else "5m"
else:
    interval_options = ["15m", "1h", "1d"]
    default_interval = "1h"
interval = st.sidebar.selectbox("Data Interval", interval_options, index=interval_options.index(default_interval), key="interval_select")

# Pattern detection sensitivity
sensitivity = st.sidebar.slider("Pattern Detection Sensitivity", 0.5, 2.0, 1.0, 0.1, help="Higher values make detection stricter")

# Technical indicators
show_sma = st.sidebar.checkbox("Show Simple Moving Average (SMA)", value=True)
show_ema = st.sidebar.checkbox("Show Exponential Moving Average (EMA)", value=False)
show_rsi = st.sidebar.checkbox("Show Relative Strength Index (RSI)", value=False)

# Custom RSI calculation
def calculate_rsi(data, periods=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# Tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["Live Data & Patterns", "Backtesting", "Technical Indicators"])

with tab1:
    st.subheader("Live Stock Data and Pattern Detection")
    if ticker:
        # Fetch data
        st.write(f"Running fetch_data({ticker}, {period}, {interval}) using Alpha Vantage...")
        data, error = fetch_alpha_vantage_data(ticker=ticker, period=period, interval=interval, api_key=ALPHA_VANTAGE_KEY)
        if error:
            st.error(error)
        elif data.empty:
            st.error(f"No data fetched for {ticker}. Try another ticker (e.g., TSLA, RELIANCE.NS), interval (e.g., 1h or 1d), or check API limits.")
        else:
            st.dataframe(data.tail())

            # Detect patterns
            patterns = detect_patterns(data, sensitivity)
            
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
            
            # Add technical indicators
            if show_sma:
                data['SMA'] = data['Close'].rolling(window=20).mean()
                fig.add_trace(go.Scatter(x=data.index, y=data['SMA'], name="SMA", line=dict(color="blue")))
            if show_ema:
                data['EMA'] = data['Close'].ewm(span=20, adjust=False).mean()
                fig.add_trace(go.Scatter(x=data.index, y=data['EMA'], name="EMA", line=dict(color="purple")))
            if show_rsi:
                data['RSI'] = calculate_rsi(data['Close'], periods=14)
                fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], name="RSI", line=dict(color="green"), yaxis="y2"))

            # Add pattern annotations
            detected_patterns = []
            for pattern, info in patterns.items():
                if info['detected']:
                    for idx in info['points']:
                        fig.add_vline(x=data.index[idx], line_dash="dash", line_color="red")
                    detected_patterns.append({"Pattern": pattern, "Action": info['action'], "Description": get_pattern_description(pattern)})
                    st.success(f"**{pattern}** detected! Suggested Action: {info['action']}")
                    with st.expander(f"Details: {pattern}"):
                        st.write(get_pattern_description(pattern))

            # Layout with secondary y-axis for RSI
            fig.update_layout(
                title=f"{ticker} Stock Chart with Pattern Detection",
                xaxis_title="Date",
                yaxis_title="Price",
                xaxis_rangeslider_visible=False,
                yaxis2=dict(title="RSI", overlaying="y", side="right", range=[0, 100], showgrid=False) if show_rsi else None
            )
            st.plotly_chart(fig, use_container_width=True)

            # Export detected patterns
            if detected_patterns:
                df_patterns = pd.DataFrame(detected_patterns)
                csv = df_patterns.to_csv(index=False)
                st.download_button("Download Detected Patterns", csv, f"{ticker}_patterns.csv", "text/csv")

            # Historical pattern comparison
            st.subheader("Historical Pattern Comparison")
            historical_fig = go.Figure()
            historical_fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name="Close Price"))
            for pattern, info in patterns.items():
                if info['detected'] and info['points']:  # Ensure points exist
                    try:
                        # Convert Timestamp to string to avoid Plotly mean calculation error
                        x_value = data.index[info['points'][-1]].strftime('%Y-%m-%d %H:%M:%S')
                        historical_fig.add_vline(x=x_value, line_dash="dot", line_color="orange", annotation_text=pattern)
                    except Exception as e:
                        logger.error(f"Error adding vline for pattern {pattern}: {str(e)}")
                        st.warning(f"Could not display historical marker for {pattern}. Please try a different ticker or interval.")
            historical_fig.update_layout(title=f"Historical Patterns for {ticker}", xaxis_title="Date", yaxis_title="Price")
            st.plotly_chart(historical_fig, use_container_width=True)

with tab2:
    st.subheader("Backtesting Results")
    if ticker and not data.empty:
        look_forward = st.slider("Look-Forward Period for Backtesting", 5, 20, 10, help="Periods to check post-pattern")
        if st.button("Run Backtest"):
            backtest_results = backtest_patterns(data, patterns, look_forward)
            for pattern, stats in backtest_results.items():
                st.write(f"**{pattern}**")
                st.write(f"Occurrences: {stats['count']}")
                st.write(f"Success Rate: {stats['success_rate']:.2%}")
                st.write(f"Average Return: {stats['avg_return']:.2%}")
            
            # Export backtest results
            df_backtest = pd.DataFrame([
                {"Pattern": pattern, "Occurrences": stats['count'], "Success Rate": stats['success_rate'], "Average Return": stats['avg_return']}
                for pattern, stats in backtest_results.items()
            ])
            csv = df_backtest.to_csv(index=False)
            st.download_button("Download Backtest Results", csv, f"{ticker}_backtest.csv", "text/csv")

with tab3:
    st.subheader("Technical Indicators")
    if ticker and not data.empty:
        st.write("**Simple Moving Average (SMA)**: 20-period average of closing prices.")
        st.write("**Exponential Moving Average (EMA)**: 20-period EMA, giving more weight to recent prices.")
        st.write("**Relative Strength Index (RSI)**: Measures momentum (0-100 scale; >70 overbought, <30 oversold).")
        if show_sma:
            st.write(f"Latest SMA: {data['SMA'].iloc[-1]:.2f}")
        if show_ema:
            st.write(f"Latest EMA: {data['EMA'].iloc[-1]:.2f}")
        if show_rsi:
            st.write(f"Latest RSI: {data['RSI'].iloc[-1]:.2f}")

# Real-time update loop (disabled by default)
if st.sidebar.checkbox("Enable Real-Time Updates", value=False):
    placeholder = st.empty()
    while True:
        data, error = fetch_alpha_vantage_data(ticker=ticker, period=period, interval=interval, api_key=ALPHA_VANTAGE_KEY)
        if not data.empty:
            placeholder.dataframe(data.tail())
        time.sleep(60)  # Update every minute
