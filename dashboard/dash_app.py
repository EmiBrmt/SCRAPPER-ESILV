import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__)

def load_data():
    df = pd.read_csv('../scraper/sp500_prices.csv', names=["Timestamp", "Price"], header=None)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['Price'] = df['Price'].astype(str).str.replace(' ', '').str.replace(',', '.').astype(float)
    return df

app.layout = html.Div(children=[
    html.H1("Évolution du prix du S&P 500"),
    dcc.Graph(id='price-graph'),
    dcc.Interval(id='interval-component', interval=5*60*1000, n_intervals=0)
])

@app.callback(
    Output('price-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n_intervals):
    df = load_data()
    fig = px.line(df, x='Timestamp', y='Price', title='Prix du S&P 500')
    return fig

if __name__ == '__main__':
    app.run(debug=True)
