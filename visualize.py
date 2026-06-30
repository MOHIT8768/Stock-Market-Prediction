import matplotlib.pyplot as plt

def plot_all_visuals(results, portfolio_allocation):
    tickers = list(results.keys())
    n = len(tickers)

    fig = plt.figure(figsize=(14, 4 * n + 4))

    #  INDIVIDUAL PRICE PREDICTION GRAPHS
    for i, ticker in enumerate(tickers):
        ax = plt.subplot2grid((n + 2, 2), (i, 0), colspan=2)

        df = results[ticker]["data"]
        predicted_price = results[ticker]["predicted_price"]

        ax.plot(
            df["Date"],
            df["Close"],
            label="Actual Price",
            linewidth=2
        )

        ax.scatter(
            df["Date"].iloc[-1],
            predicted_price,
            color="red",
            edgecolor="black",
            linewidth=1.5,
            s=100,
            label="Predicted Price",
            zorder=5
        )

        ax.set_title(f"{ticker} – Price Prediction")
        ax.set_ylabel("Price")
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.6)

    #  RISK BAR CHART (WITH EDGES)
    risks = [results[t]["risk"] for t in tickers]

    ax_risk = plt.subplot2grid((n + 2, 2), (n, 0))
    ax_risk.bar(
        tickers,
        risks,
        edgecolor="black",
        linewidth=1.5
    )
    ax_risk.set_title(" Risk (Volatility)")
    ax_risk.set_ylabel("Risk")
    ax_risk.grid(axis="y", linestyle="--", alpha=0.6)

    #  RETURN BAR CHART (WITH EDGES)
    returns = [results[t]["return"] for t in tickers]

    ax_return = plt.subplot2grid((n + 2, 2), (n, 1))
    ax_return.bar(
        tickers,
        returns,
        edgecolor="black",
        linewidth=1.5
    )
    ax_return.set_title(" Expected Return (%)")
    ax_return.set_ylabel("Return (%)")
    ax_return.grid(axis="y", linestyle="--", alpha=0.6)

    #  PORTFOLIO ALLOCATION BAR CHART (WITH EDGES)
    allocations = [portfolio_allocation.get(t, 0) * 100 for t in tickers]

    ax_alloc = plt.subplot2grid((n + 2, 2), (n + 1, 0), colspan=2)
    ax_alloc.bar(
        tickers,
        allocations,
        edgecolor="black",
        linewidth=1.5
    )
    ax_alloc.set_title(" Quantum-Inspired Portfolio Allocation (%)")
    ax_alloc.set_ylabel("Allocation (%)")
    ax_alloc.grid(axis="y", linestyle="--", alpha=0.6)

    plt.tight_layout()
    plt.show()
