import yfinance as yf
import pandas as pd
import requests

#  PUT YOUR REAL ALPHA VANTAGE API KEY HERE
ALPHA_VANTAGE_API_KEY = "J7MXZ7E7LM36L07P"

# User-friendly ticker mapping
TICKER_MAP = {
    "NIFTY 50": "^NSEI",
    "NIFTY": "^NSEI",
    "SENSEX": "^BSESN",
    "BANKNIFTY": "^NSEBANK",
    "BANK NIFTY": "^NSEBANK",
}

def fetch_from_alpha_vantage(ticker):
    print(" Falling back to Alpha Vantage...")

    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker,
        "apikey": ALPHA_VANTAGE_API_KEY,
        "outputsize": "compact"
    }

    response = requests.get(url, params=params, timeout=20)
    data = response.json()

    if "Time Series (Daily)" not in data:
        print(" Alpha Vantage failed or API limit reached")
        return None

    ts = data["Time Series (Daily)"]
    df = pd.DataFrame.from_dict(ts, orient="index")

    df = df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume"
    })

    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df.reset_index(inplace=True)
    df.rename(columns={"index": "Date"}, inplace=True)

    df[["Open", "High", "Low", "Close", "Volume"]] = df[
        ["Open", "High", "Low", "Close", "Volume"]
    ].astype(float)

    return df

def fetch_live_data(ticker, period="5d", interval="5m"):
    ticker = ticker.upper().strip()
    ticker = TICKER_MAP.get(ticker, ticker)

    # Indices do NOT support intraday
    if ticker.startswith("^"):
        interval = "1d"
        period = "6mo"

    try:
        print(f"📡 Fetching data for {ticker} ({interval})...")
        df = yf.download(
            ticker,
            period=period,
            interval=interval,
            progress=False
        )

        if df.empty:
            raise ValueError("Empty data")

        df.reset_index(inplace=True)

        time_col = "Datetime" if "Datetime" in df.columns else "Date"
        return df[[time_col, "Open", "High", "Low", "Close", "Volume"]]

    except Exception as e:
        print(f"❌ Data fetch failed for {ticker}: {e}")
        return None


