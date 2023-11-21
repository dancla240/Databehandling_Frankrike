from dash import Dash, html, dcc, callback, Input, Output, dash_table, page_registry, page_container
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash_bootstrap_templates import load_figure_template

athlete_events = pd.read_csv('Data/athlete_events.csv')


load_figure_template("flatly")

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], use_pages=True)

app.layout = dbc.Container([
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in page_registry.values()
    ]),
    page_container,
])

if  __name__ == "__main__":
    app.run(debug=True, port=8051)