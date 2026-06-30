import plotly.graph_objects as go
import os
import subprocess

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def open_dashboard(portfolio_allocation, risks, returns):
    tickers = list(portfolio_allocation.keys())

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=tickers,
            y=[portfolio_allocation[t]*100 for t in tickers],
            name="Portfolio Allocation (%)",
            marker=dict(line=dict(color="black", width=2))
        )
    )

    fig.add_trace(
        go.Bar(
            x=tickers,
            y=[risks[t] for t in tickers],
            name="Risk",
            marker=dict(line=dict(color="black", width=2))
        )
    )

    fig.add_trace(
        go.Bar(
            x=tickers,
            y=[returns[t] for t in tickers],
            name="Expected Return (%)",
            marker=dict(line=dict(color="black", width=2))
        )
    )

    fig.update_layout(
        title="Portfolio Risk–Return Dashboard",
        barmode="group",
        template="plotly_dark",
        height=600
    )

    file_path = os.path.abspath("dashboard.html")
    fig.write_html(file_path, auto_open=False)
    subprocess.Popen([EDGE_PATH, file_path])
