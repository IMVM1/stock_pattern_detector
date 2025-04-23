# Real-Time Chart Pattern Detection Tool

A Python-based web application built with Streamlit to detect chart patterns in real-time stock data, provide visual alerts, send Telegram notifications, and perform backtesting.

## Features
- **Real-Time Data**: Fetches stock data using the Yahoo Finance API (`yfinance`).
- **Pattern Detection**:
  - Double Top / Double Bottom
  - Head & Shoulders
  - Flag & Pennant
  - Triangles
  - Cup & Handle
- **Visual Alerts**: Interactive candlestick charts with pattern annotations using Plotly.
- **Notifications**: Telegram alerts for detected patterns using a hardcoded bot token and chat ID.
- **Backtesting**: Evaluates pattern reliability on historical data.
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
- **Telegram Notifications**: The Telegram bot token and chat ID are hardcoded in `app.py`. Ensure the bot is set up correctly:
  - Verify the bot token (`7424007039:AAG62YomUNo2ipomDJsUk-nlDCDEiky6IS0`) via `@BotFather`.
  - Confirm the chat ID (`charts_pattern_bot`) is correct by messaging the bot.
- **Stock Ticker**: Enter any valid stock ticker (e.g., AAPL, TSLA) in the Streamlit sidebar.
- **Data Interval/Period**: Select the desired data granularity and lookback period.

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
   - Specify the main file (`app.py`).
   - Deploy the app.

## Notes
- The pattern detection algorithms are simplified for demonstration. Enhance them with more sophisticated logic for production use.
- Real-time updates are simulated with a 60-second refresh due to API limitations.
- Ensure compliance with Yahoo Finance API terms of service.
- For security, consider moving the Telegram token and chat ID to environment variables in a production environment.

## License
MIT License