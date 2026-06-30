# quantum_optimizer.py
# Quantum-Inspired Portfolio Optimization (Final Stable Version)

import numpy as np

def quantum_portfolio_optimize(tickers, values):
    """
    Quantum-inspired portfolio optimization.

    Parameters:
    - tickers : list of str
        Stock / index tickers
    - values : list of float
        Importance values (e.g., abs(expected return) or price difference)

    Returns:
    - dict with portfolio allocation per ticker
    """

    values = np.array(values, dtype=float)

    # Handle edge cases
    if len(values) == 0:
        return {
            "portfolio_allocation": {},
            "note": "No valid inputs for optimization"
        }

    if np.all(values == 0):
        equal_weight = 1.0 / len(values)
        return {
            "portfolio_allocation": {
                t: equal_weight for t in tickers
            },
            "note": "All values zero – equal weight allocation used"
        }

    # -------- Quantum-Inspired Normalization --------
    # Amplitudes (superposition)
    amplitudes = values / np.linalg.norm(values)

    # Measurement probabilities
    probabilities = amplitudes ** 2

    # Normalize again (numerical safety)
    probabilities = probabilities / probabilities.sum()

    # Map to tickers
    portfolio_allocation = {
        ticker: float(round(prob, 6))
        for ticker, prob in zip(tickers, probabilities)
    }

    return {
        "portfolio_allocation": portfolio_allocation,
        "note": "Quantum-inspired portfolio optimization using probability amplitudes"
    }
