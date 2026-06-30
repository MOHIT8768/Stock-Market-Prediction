# web_stock_page.py
# Final fixed line chart (NO pandas ambiguity)

import plotly.graph_objects as go
import os
import subprocess
import time
import pandas as pd

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def open_stock_page(ticker, data, predicted_price):
    # Ensure datetime index
    if not isinstance(data.index, pd.DatetimeIndex):
        data.index = pd.to_datetime(data.index)

    x_actual = data.index
    y_actual = data["Close"].astype(float).values

    # Future timestamp for prediction
    if len(x_actual) > 1:
        future_time = x_actual[-1] + (x_actual[-1] - x_actual[-2])
    else:
        future_time = x_actual[-1]

    # Safe Y-axis scaling
    y_min = min(float(y_actual.min()), float(predicted_price))
    y_max = max(float(y_actual.max()), float(predicted_price))

    padding = (y_max - y_min) * 0.25 if y_max != y_min else y_max * 0.05

    fig = go.Figure()

    # 🔴 Actual price line
    fig.add_trace(
        go.Scatter(
            x=x_actual,
            y=y_actual,
            mode="lines",
            line=dict(color="red", width=3),
            name="Actual Price"
        )
    )

    # 🟢 Predicted price bubble
    fig.add_trace(
        go.Scatter(
            x=[future_time],
            y=[float(predicted_price)],
            mode="markers+text",
            marker=dict(
                size=40,
                color="green",
                line=dict(color="black", width=2)
            ),
            text=[f"Predicted: {predicted_price:.2f}"],
            textposition="top center",
            name="Predicted Price"
        )
    )

    fig.update_layout(
        title=f"{ticker} Price Prediction (Line Chart)",
        xaxis_title="Time",
        yaxis_title="Price",
        template="plotly_dark",
        height=650,
        yaxis=dict(
            range=[y_min - padding, y_max + padding],
            tickformat=".2f",
            showgrid=True
        ),
        xaxis=dict(showgrid=True),
        legend=dict(x=0.02, y=0.98)
    )

    file_name = f"stock_{ticker.replace(' ', '_')}.html"
    file_path = os.path.abspath(file_name)

    fig.write_html(file_path, auto_open=False)

    time.sleep(1)
    subprocess.Popen([EDGE_PATH, "--new-tab", file_path])
