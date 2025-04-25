# Real-Time Chart Pattern Detection Tool

A Python-based web application built with Streamlit to detect chart patterns in real-time stock data using the Alpha Vantage API, providing visual alerts, technical indicators, historical comparisons, and backtesting with exportable results.

## Features
- **Real-Time Data**: Fetches stock data using Alpha Vantage with retry logic and ticker validation.
- **Pattern Detection**:
  - Double Top / Double Bottom
  - Head & Shoulders
  - Flag & Pennant
  - Triangles
  - Cup & Handle
- **Visual Alerts**: Interactive candlestick charts with pattern annotations using Plotly.
- **Technical Indicators**: SMA, EMA, and RSI using pandas.
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
- **Data Interval/Period**: Valid combinations:
  - 1m: 1d, 5d (market hours: 9:30 AM - 4:00 PM ET, Mon-Fri)
  - 5m: 1d, 5d, 1mo
  - 15m, 1h, 1d: 1d, 5d, 1mo, 3mo, 6mo
- **Sensitivity**: Adjust pattern detection strictness (0.5 to 2.0).
- **Indicators**: Toggle SMA, EMA, and RSI.

## Alpha Vantage Setup
- The app uses a hardcoded Alpha Vantage API key (`Y7VITAXN4E37H0L4`) for testing.
- For production, get your own free API key at [Alpha Vantage](https://www.alphavantage.co/support/#api-key).
- Replace the key in `app.py`:
  ```python
  ALPHA_VANTAGE_KEY = "YOUR_API_KEY"
  ```
- Free tier limits: 5 API calls per minute, 500 per day. Upgrade for higher limits.

## Deployment
1. **Push to GitHub**:
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
   - Set **Main Python file** to `app.py`.
   - Deploy the app.
3. **Fix Main Module Issue**:
   - If logs show errors, go to **Manage app** > **App settings**.
   - Ensure **Main Python file** is `app.py`.
   - Reboot the app.

## Troubleshooting
- **No Data Fetched**:
  - **Verify Settings**: Ensure valid ticker (e.g., AAPL, RELIANCE.NS), period (e.g., 5d), and interval (e.g., 15m).
  - **Market Hours**: Test 1m data during US market hours (9:30 AM - 4:00 PM ET, Mon-Fri).
  - **Alpha Vantage**:
    - Verify API key is valid at [Alpha Vantage](https://www.alphavantage.co).
    - Check API limits (5 calls/min, 500/day). If "limit reached" error, wait 1–2 minutes.
    - Test alternative tickers (e.g., TSLA, MSFT) or intervals (e.g., 1h, 1d).
    - Check logs for errors (e.g., "Invalid API call", "No time series data").
  - Test locally: `streamlit run app.py` and check terminal logs.
  - Use a VPN to rule out regional blocks.
- **Code Errors**:
  - Ensure latest `app.py` and `data_fetcher.py` are deployed.
  - Check logs for runtime errors.
- **Requirements Error**:
  - Verify `requirements.txt` matches listed versions (e.g., `alpha_vantage==3.0.0`).
  - Check Streamlit logs under **Manage App** > **Logs**.
- **Streamlit Cloud**:
  - Clear cache: **Manage app** > **Advanced settings** > **Clear cache**.
  - Reboot after updates.
  - Confirm `app.py` is the main file.

## Notes
- Pattern detection is simplified. Enhance with ML for production.
- Real-time updates are disabled by default to reduce API load.
- Comply with Alpha Vantage API terms.

## License
MIT License