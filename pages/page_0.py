from dash import Dash, html, dcc, callback, Input, Output, register_page, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash_bootstrap_templates import load_figure_template

athlete_events = pd.read_csv('Data/athlete_events.csv')
athlete_events.sort_values(by='Year', inplace=True, ascending=False)

# Load the 'flatly' theme for the Dash application
load_figure_template("flatly")

# Initialize a Dash app with the 'flatly' theme
register_page(__name__, 
            path='/page_0',
            title='Home Page',
            name='Home Page')

# Define the layout of the app using the Dash Bootstrap Components (dbc)
layout = dbc.Container([
    dbc.Row([
        html.H2('Antalet länder som har deltagit:'),
        html.H3(athlete_events['NOC'].nunique())
    ]),

    dbc.Row([
        html.H2('Länder:'),
        html.H3(list(athlete_events['NOC'].unique())),
    ]),
], fluid=True)