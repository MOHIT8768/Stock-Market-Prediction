import yfinance as yf
import pandas as pd
import numpy as np
from scipy.stats import norm
import math

def black_scholes(S, K, T, r, sigma, option_type="call"):
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    if option_type == "call":
        return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    else:
        return K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

def predict_option_chain(ticker, predicted_price, r=0.05):
    stock = yf.Ticker(ticker)
    expiries = stock.options

    if not expiries:
        print(" No options available")
        return None

    expiry = expiries[0]  # nearest expiry
    opt_chain = stock.option_chain(expiry)

    calls = opt_chain.calls[['strike', 'impliedVolatility']].copy()
    puts = opt_chain.puts[['strike', 'impliedVolatility']].copy()


    T = 7 / 365  # assume 1 week to expiry

    calls['Predicted Call Price'] = calls.apply(
        lambda row: black_scholes(
            predicted_price,
            row['strike'],
            T,
            r,
            row['impliedVolatility'],
            "call"
        ),
        axis=1
    )

    puts['Predicted Put Price'] = puts.apply(
        lambda row: black_scholes(
            predicted_price,
            row['strike'],
            T,
            r,
            row['impliedVolatility'],
            "put"
        ),
        axis=1
    )

    return calls, puts
