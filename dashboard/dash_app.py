import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# === Chargement manuel ligne par ligne ===
timestamps = []
prices = []

with open("/home/ec2-user/SCRAPPER-ESILV/scraper/sp500_prices.csv", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split(",", 1)  # couper UNIQUEMENT à la première virgule
        if len(parts) == 2:
            ts = parts[0].strip()
            price = parts[1].strip().replace(" ", "").replace(",", ".")
            try:
                timestamps.append(pd.to_datetime(ts, format="%Y-%m-%d %H:%M:%S"))
                prices.append(float(price))
            except Exception as e:
                print(f"Ligne ignorée : {line.strip()} - Erreur : {e}")

# === Création du DataFrame final ===
df = pd.DataFrame({"timestamp": timestamps, "price": prices})

# === Création du graphique ===
fig = px.line(df, x="timestamp", y="price", title="Évolution du prix du S&P 500")

# === App Dash ===
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Évolution du prix du S&P 500"),
    dcc.Graph(figure=fig)
])

# === Run server ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)
