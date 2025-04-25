import pandas as pd
import requests
import time
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Check if current time is within US market hours (9:30 AM - 4:00 PM ET, Mon-Fri)
def is_market_open():
    now = datetime.now().astimezone(tz=None)
    market_open = datetime.strptime("09:30", "%H:%M").time()
    market_close = datetime.strptime("16:00", "%H:%M").time()
    return now.weekday() < 5 and market_open <= now.time() <= market_close

# Map Streamlit intervals to Alpha Vantage intervals
ALPHA_VANTAGE_INTERVALS = {
    "1m": "1min",
    "5m": "5min",
    "15m": "15min",
    "1h": "60min",
    "1d": "daily"
}

# Validate period/interval compatibility
VALID_COMBINATIONS = {
    "1m": ["1d", "5d"],
    "5m": ["1d", "5d", "1mo"],
    "15m": ["1d", "5d", "1mo", "3mo", "6mo"],
    "1h": ["1d", "5d", "1mo", "3mo", "6mo"],
    "1d": ["1d", "5d", "1mo", "3mo", "6mo"]
}

def fetch_alpha_vantage_data(ticker, period, interval, api_key, retries=3):
    if not ticker:
        return pd.DataFrame(), "Please enter a valid ticker (e.g., AAPL, RELIANCE.NS)."
    if not api_key:
        return pd.DataFrame(), "Alpha Vantage API key is required."
    
    if interval not in VALID_COMBINATIONS or period not in VALID_COMBINATIONS[interval]:
        return pd.DataFrame(), f"Invalid interval {interval} for period {period}. Use 1m or 5m for 1d/5d, or 15m/1h for longer periods."

    if interval == "1m" and not is_market_open():
        return pd.DataFrame(), f"1m data for {ticker} is only available during US market hours (9:30 AM - 4:00 PM ET, Mon-Fri). Try 5m or 15m."

    av_interval = ALPHA_VANTAGE_INTERVALS.get(interval)
    if not av_interval:
        return pd.DataFrame(), f"Unsupported interval {interval} for Alpha Vantage."

    # Map period to Alpha Vantage output size
    output_size = "compact" if period in ["1d", "5d"] else "full"
    
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_INTRADAY" if interval in ["1m", "5m", "15m", "1h"] else "TIME_SERIES_DAILY",
        "symbol": ticker,
        "interval": av_interval if interval in ["1m", "5m", "15m", "1h"] else None,
        "outputsize": output_size,
        "apikey": api_key,
        "datatype": "json"
    }
    
    try:
        for attempt in range(retries):
            try:
                response = requests.get(base_url, params=params)
                response.raise_for_status()
                data = response.json()
                
                # Check for API errors
                if "Error Message" in data:
                    return pd.DataFrame(), f"Alpha Vantage error: {data['Error Message']}. Check ticker or API key."
                if "Note" in data:
                    logger.warning(f"Alpha Vantage limit reached: {data['Note']}")
                    if attempt < retries - 1:
                        time.sleep(60)  # Wait 1 minute for API limit reset
                        continue
                    return pd.DataFrame(), f"Alpha Vantage API limit reached: {data['Note']}. Wait 1–2 minutes or upgrade to premium."
                
                # Parse data
                time_series_key = next((key for key in data if "Time Series" in key), None)
                if not time_series_key:
                    return pd.DataFrame(), f"No time series data found for {ticker}. Check ticker or API availability."
                
                df = pd.DataFrame.from_dict(data[time_series_key], orient="index")
                df = df.rename(columns={
                    "1. open": "Open",
                    "2. high": "High",
                    "3. low": "Low",
                    "4. close": "Close",
                    "5. volume": "Volume"
                })
                df = df.astype(float)
                df.index = pd.to_datetime(df.index, utc=True).tz_convert(None)  # Ensure timezone-naive index
                df = df.sort_index()
                
                # Filter data based on period
                if period != "6mo":
                    period_map = {"1d": 1, "5d": 5, "1mo": 30, "3mo": 90}
                    days = period_map.get(period, 180)
                    try:
                        # Use timezone-naive Timestamp for cutoff
                        cutoff = pd.Timestamp.now().tz_localize(None) - pd.Timedelta(days=days)
                        if not isinstance(df.index, pd.DatetimeIndex):
                            logger.error(f"DataFrame index is not DatetimeIndex: {type(df.index)}")
                            return pd.DataFrame(), f"Invalid DataFrame index for {ticker}. Contact support."
                        logger.debug(f"Filtering data for {ticker}: index dtype={df.index.dtype}, cutoff={cutoff}, cutoff dtype={type(cutoff)}")
                        df = df[df.index >= cutoff]
                    except Exception as e:
                        logger.error(f"Error filtering data for {ticker}: {str(e)}")
                        return pd.DataFrame(), f"Error filtering data for {ticker}: {str(e)}. Try a different period (e.g., 5d) or interval (e.g., 15m)."
                
                if df.empty:
                    return pd.DataFrame(), f"No Alpha Vantage data for {ticker} with interval {interval}. Try another interval or ticker."
                
                logger.info(f"Successfully fetched Alpha Vantage data for {ticker} with interval {interval}")
                return df, None
            except (requests.RequestException, ValueError) as e:
                logger.error(f"Attempt {attempt + 1}: Error fetching Alpha Vantage data for {ticker}: {str(e)}")
                time.sleep(10)
        
        error_msg = (f"Failed to fetch Alpha Vantage data for {ticker} with interval {interval} after {retries} attempts. "
                     "Check ticker, API key, or try another interval (e.g., 1h or 1d).")
        logger.error(error_msg)
        return pd.DataFrame(), error_msg
    except Exception as e:
        error_msg = f"Error fetching Alpha Vantage data for {ticker}: {str(e)}. Check API key, network, or ticker."
        logger.error(error_msg)
        return pd.DataFrame(), error_msg