# main.py
# Hybrid Classical–Quantum Stock Prediction System (Final Stable Version)

from fetch_data import fetch_live_data
from classical_predictor import classical_predict
from option_chain_predictor import predict_option_chain
from quantum_optimizer import quantum_portfolio_optimize
from web_stock_page import open_stock_page

def call_put_reason(current_price, predicted_price):
    if predicted_price > current_price:
        return "CALL", "Predicted price is above current price : Bullish (buy / long)"
    else:
        return "PUT", "Predicted price is below current price : Bearish (sell / short)"

def main():
    print("\n📈 Hybrid Classical-Quantum Stock Prediction System\n")

    # -------- USER INPUT --------
    tickers = input(
        "Enter stock/index tickers (e.g : AAPL,MSFT,AMZN,NIFTY 50,GOOGL,F): "
    ).upper().split(",")

    interval = input(
        "Choose time interval (5m / 10m / 15m / 30m  / 1d): "
    ).strip()

    option_choice = input(
        "Do you want Option Chain Prediction? (yes/no): "
    ).lower().strip()

    # -------- INTERVAL FIX (IMPORTANT) --------
    INTERVAL_MAP = {
        "10m": "15m",   # Yahoo does NOT support 10m
        "20m": "30m"
    }

    if interval in INTERVAL_MAP:
        print(f"⚠️ Interval '{interval}' not supported. Switching to '{INTERVAL_MAP[interval]}'")
        interval = INTERVAL_MAP[interval]

    # -------- PERIOD LOGIC --------
    PERIOD_MAP = {
        "5m": "5d",
        "15m": "5d",
        "30m": "1mo",
        "1d": "6mo"
    }

    period = PERIOD_MAP.get(interval, "1mo")

    # -------- FOR QUANTUM OPTIMIZATION --------
    optimization_inputs = {}

    # -------- PROCESS EACH TICKER --------
    for ticker in tickers:
        ticker = ticker.strip()
        print(f"\n🔍 Processing {ticker}...")

        data = fetch_live_data(ticker, period, interval)

        if data is None:
            print(f"❌ Data fetch failed for {ticker}")
            print(f"❌ Skipping {ticker} (no data)")
            continue

        if data.empty:
            print(f"❌ Empty data returned for {ticker}")
            print(f"❌ Skipping {ticker} (no data)")
            continue

        data = data.dropna()

        # -------- PREDICTION --------
        predicted_price = classical_predict(data)
        current_price = data["Close"].iloc[-1].item()

        signal, reason = call_put_reason(current_price, predicted_price)

        print(f"Current Price: {current_price:.2f}")
        print(f"Predicted Price: {predicted_price:.2f}")
        print(f"Signal: {signal} → {reason}")

        # -------- OPTION CHAIN (SAFE) --------
        if option_choice == "yes":
            option_result = predict_option_chain(ticker, predicted_price)

            if option_result is None:
                print("No options available")
            else:
                calls, puts = option_result
                print("Calls:")
                print(calls.head())
                print("Puts:")
                print(puts.head())

        # -------- OPEN GRAPH (EDGE) --------
        open_stock_page(ticker, data, predicted_price)

        # -------- FOR OPTIMIZATION --------
        optimization_inputs[ticker] = abs(predicted_price - current_price)

    # -------- QUANTUM-INSPIRED OPTIMIZATION --------
    if len(optimization_inputs) > 1:
        result = quantum_portfolio_optimize(
            list(optimization_inputs.keys()),
            list(optimization_inputs.values())
        )

        print("\n⚛️ Quantum-Inspired Portfolio Optimization:")
        for t, w in result["portfolio_allocation"].items():
            print(f"  {t} → {w * 100:.2f}%")

    print("\n✅ Execution completed successfully")

# -------- ENTRY POINT --------
if __name__ == "__main__":
    main()
