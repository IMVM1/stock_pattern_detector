# Real-Time Chart Pattern Detection Tool

A Python-based web application built with Streamlit to detect chart patterns in real-time stock data, provide visual alerts, technical indicators, historical comparisons, and backtesting with exportable results.

## Features
- **Real-Time Data**: Fetches stock data using the Yahoo Finance API (`yfinance`) with retry logic and ticker validation.
- **Pattern Detection**:
  - Double Top / Double Bottom
  - Head & Shoulders
  - Flag & Pennant
  - Triangles
  - Cup & Handle
- **Visual Alerts**: Interactive candlestick charts with pattern annotations using Plotly.
- **Technical Indicators**: Simple Moving Average (SMA), Exponential Moving Average (EMA), and Relative Strength Index (RSI) using pandas.
- **Export Results**: Download detected patterns and backtest results as CSV.
- **Historical Comparison**: Visualize historical pattern occurrences.
- **Customization**: Adjustable pattern detection sensitivity and backtesting parameters.
- **UI**: Tabbed interface for live data, backtesting, and indicators.
- **Deployment**: Deployable on Streamlit Community Cloud.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/stock_pattern_detector.git
   cd stock_pattern_detector
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Run the Streamlit app locally:
   ```bash
   streamlit run app.py
   ```

## Configuration
- **Stock Ticker**: Select from a list (e.g., AAPL, RELIANCE.NS) or enter a custom ticker.
- **Data Interval/Period**: Choose granularity and lookback period. Valid combinations:
  - 1m: 1d, 5d (only during US market hours: 9:30 AM - 4:00 PM ET, Mon-Fri)
  - 5m: 1d, 5d, 1mo
  - 15m, 1h, 1d: 1d, 5d, 1mo, 3mo, 6mo
- **Sensitivity**: Adjust pattern detection strictness (0.5 to 2.0).
- **Indicators**: Toggle SMA, EMA, and RSI on charts.

## Deployment
1. **Push to GitHub**:
   - Create a new repository on GitHub.
   - Push the project:
     ```bash
     git init
     git add .
     git commit -m "Initial commit"
     git branch -M main
     git remote add origin https://github.com/yourusername/stock_pattern_detector.git
     git push -u origin main
     ```
2. **Deploy on Streamlit Community Cloud**:
   - Sign up at [Streamlit Community Cloud](https://streamlit.io/cloud).
   - Connect your GitHub account.
   - Select the repository and branch (`main`).
   - Specify the main file as `app.py`.
   - Deploy the app.
3. **Fix Main Module Issue**:
   - If the app fails (e.g., logs show `pattern_detector.py`), update:
     - Go to **Manage app** > **App settings**.
     - Set **Main Python file** to `app.py`.
     - Reboot the app.

## Troubleshooting
- **No Data Fetched or Invalid Ticker**:
  - Ensure the ticker is valid (e.g., AAPL, RELIANCE.NS, TSLA).
  - Check interval/period compatibility:
    - Use 1m only for 1d or 5d during US market hours (9:30 AM - 4:00 PM ET, Mon-Fri).
    - Use 5m for 1d, 5d, or 1mo; try 15m or 1h if 5m fails.
    - Use 15m or 1h for longer periods (e.g., 3mo, 6mo).
  - If "No data" errors persist (e.g., for AAPL with 5m):
    - Try a different interval (e.g., 15m or 1h).
    - Check market hours, as data availability may be limited outside 9:30 AM - 4:00 PM ET.
    - Wait 10–15 minutes and retry, as Yahoo Finance API may be rate-limited or down.
    - Test locally with `streamlit run app.py` to isolate Streamlit Cloud issues.
    - Update `yfinance`: `pip install --upgrade yfinance`.
    - Check Streamlit logs for `yfinance` errors (e.g., JSONDecodeError, HTTP 403, 429).
  - Verify network connectivity or try a different network/VPN.
  - Consider alternative APIs (e.g., Alpha Vantage) if issues persist.
- **Code Errors**:
  - If errors like "type object 'datetime.time' has no attribute 'sleep'" appear, ensure the latest `app.py` is deployed.
  - Check Streamlit logs for runtime or syntax errors.
- **Requirements Error**:
  - Verify `requirements.txt` matches the listed versions.
  - Check Streamlit Cloud logs under **Manage App** > **Logs**.
- **Local Testing**:
  - Run `streamlit run app.py` locally to debug.
  - Upgrade `yfinance` if needed: `pip install --upgrade yfinance`.

## Notes
- Pattern detection is simplified. Enhance with ML models for production.
- Real-time updates are disabled by default to reduce API load. Enable only when needed.
- Ensure compliance with Yahoo Finance API terms.

## License
MIT License