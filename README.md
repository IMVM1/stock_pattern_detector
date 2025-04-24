Real-Time Chart Pattern Detection Tool
A Python-based web application built with Streamlit to detect chart patterns in real-time stock data, provide visual alerts, send Telegram notifications, and perform backtesting.
Features

Real-Time Data: Fetches stock data using the Yahoo Finance API (yfinance).
Pattern Detection:
Double Top / Double Bottom
Head & Shoulders
Flag & Pennant
Triangles
Cup & Handle


Visual Alerts: Interactive candlestick charts with pattern annotations using Plotly.
Notifications: Telegram alerts for detected patterns using a hardcoded bot token and chat ID.
Backtesting: Evaluates pattern reliability on historical data.
Deployment: Deployable on Streamlit Community Cloud.

Installation

Clone the repository:git clone https://github.com/yourusername/stock_pattern_detector.git
cd stock_pattern_detector


Create a virtual environment and install dependencies:python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt


Run the Streamlit app locally:streamlit run app.py



Configuration

Telegram Notifications: The Telegram bot token is hardcoded in app.py. Update the chat ID:
Verify the bot token (7424007039:AAG62YomUNo2ipomDJsUk-nlDCDEiky6IS0) via @BotFather.
Obtain the numeric chat ID by messaging the bot and checking https://api.telegram.org/bot<TOKEN>/getUpdates or using @userinfobot.
Replace YOUR_NUMERIC_CHAT_ID in app.py with the correct chat ID.


Stock Ticker: Enter any valid stock ticker (e.g., AAPL, TSLA) in the Streamlit sidebar.
Data Interval/Period: Select the desired data granularity and lookback period.

Deployment

Push to GitHub:
Create a new repository on GitHub.
Push the project:git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/stock_pattern_detector.git
git push -u origin main




Deploy on Streamlit Community Cloud:
Sign up at Streamlit Community Cloud.
Connect your GitHub account.
Select the repository and branch (main).
Specify the main file as app.py (not pattern_detector.py).
Deploy the app.


Fix Main Module Issue:
If the app fails to start, ensure the main file is set to app.py in Streamlit Cloud:
Go to Manage app > App settings.
Set Main Python file to app.py.
Reboot the app.





Notes

The pattern detection algorithms are simplified for demonstration. Enhance them with more sophisticated logic for production use.
Real-time updates are simulated with a 60-second refresh due to API limitations.
Ensure compliance with Yahoo Finance API terms of service.
For security, consider moving the Telegram token and chat ID to environment variables in a production environment (e.g., using python-dotenv).

License
MIT License
