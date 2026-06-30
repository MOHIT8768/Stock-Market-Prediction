# classical_predictor.py
# Safe classical price prediction (handles empty data)

import numpy as np
from sklearn.linear_model import LinearRegression

def classical_predict(data):
    """
    Predict next price using simple linear regression.
    Returns last close price if data is insufficient.
    """

    # Safety check
    if data is None or data.empty or len(data) < 5:
        # Fallback: return last known price
        return float(data["Close"].iloc[-1]) if data is not None and not data.empty else 0.0

    # Use index as time feature
    X = np.arange(len(data)).reshape(-1, 1)
    y = data["Close"].values

    # Another safety check
    if len(X) == 0 or len(y) == 0:
        return float(data["Close"].iloc[-1])

    # Train model
    model = LinearRegression()
    model.fit(X, y)

    # Predict next time step
    next_step = np.array([[len(data)]])
    predicted_price = model.predict(next_step)[0]

    return float(predicted_price)
