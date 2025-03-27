import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import os

app = dash.Dash(__name__)
app.title = "S&P 500 Tracker"

csv_path = "/home/ec2-user/SCRAPPER-ESILV/scraper/sp500_prices.csv"

def load_data():
    timestamps = []
    prices = []

    if not os.path.exists(csv_path):
        return pd.DataFrame(columns=["timestamp", "price"])

    with open(csv_path, encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(",", 1)
            if len(parts) == 2:
                ts = parts[0].strip()
                price = parts[1].strip().replace(" ", "").replace(",", ".")
                try:
                    dt = pd.to_datetime(ts, format="%Y-%m-%d %H:%M:%S", utc=True)
                    dt_local = dt.tz_convert("Europe/Paris")
                    timestamps.append(dt_local)
                    prices.append(float(price))
                except:
                    continue

    return pd.DataFrame({"timestamp": timestamps, "price": prices})


app.layout = html.Div(style={
    "backgroundColor": "#0d1117",
    "color": "#f0f6fc",
    "fontFamily": "Segoe UI, Roboto, sans-serif",
    "padding": "30px"
}, children=[
    html.H1("📈 S&P 500 Tracker — La Défense Edition", style={
        "textAlign": "center",
        "fontWeight": "bold",
        "fontSize": "36px",
        "marginBottom": "10px"
    }),

    html.Div(id="last-price", style={
        "textAlign": "center",
        "fontSize": "24px",
        "marginBottom": "30px",
        "color": "#58a6ff"
    }),

    dcc.Graph(id="price-graph", config={"displayModeBar": False}),
    dcc.Interval(id="interval", interval=2*60*1000, n_intervals=0)  # 2 minutes
])


@app.callback(
    Output("price-graph", "figure"),
    Output("last-price", "children"),
    Input("interval", "n_intervals")
)
def update_graph(_):
    df = load_data()
    if df.empty:
        return go.Figure(), "Données non disponibles"

    last_price = df["price"].iloc[-1]
    last_time = df["timestamp"].iloc[-1].strftime("%H:%M:%S")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["timestamp"],
        y=df["price"],
        mode="lines+markers",
        line=dict(color="#58a6ff", width=2),
        marker=dict(size=4)
    ))

    fig.update_layout(
        paper_bgcolor="#0d1117",
        plot_bgcolor="#0d1117",
        font=dict(color="#f0f6fc"),
        margin=dict(t=30, r=10, l=10, b=40),
        xaxis=dict(title="Heure", showgrid=False),
        yaxis=dict(title="Prix", showgrid=True, gridcolor="#2e3440"),
    )

    display = f"Dernier prix : {last_price:.2f} — {last_time}"
    return fig, display


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)
