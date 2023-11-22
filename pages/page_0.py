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
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.H3('Grupp Frankrike:', style={'font-weight': 'bold'}),
            html.P('Medlemmar: Asajad, Arsen, Daniel.', style={})
        ], width=4, style={'box-shadow': '0px 0px 14px 5px rgba(32,73,179,0.75)', 'text-align': 'center'}),
        dbc.Col([
            html.H1('Olympiska Spelen', style={'font-weight': 'bold', 'color': 'rgba(32,73,179,0.75)', 'text-align': 'center', 'padding-top': '10px'}),
        ], width=7, style={'box-shadow': '0px 0px 14px 5px rgba(32,73,179,0.75)', 'margin-left': 'auto'}),
    ]),
    html.Br(),
    dbc.Row([
        html.H3(html.U('Frågeställningar Frankrike:'), style={'font-weight': 'bold'}),
        html.P('1. Vilken eller vilka sporter har Frankrike varit mest framgångsrikt i?'),
        html.P('2. Har Frankrike varit mest framgångsrikt i sommar eller vinter OS?'),
        html.P('3. Finns det någon tid i historien som kan sägas vara Frankrikes storhetstid i OS?'),
        html.P('4. Vilket var Frankrikes bästa OS?'),
        html.P('5. Hur ser könsfördelningen ut i olika sportgrenar?'),
        html.P('6. Hur ser åldersfördelningen ut för Frankrike genom åren?'),
    ], style={'box-shadow': '0px 0px 14px 5px rgba(32,73,179,0.75)', 'text-align': 'center'}),
    html.Br(),
    dbc.Row([
        html.H3(html.U('Frågeställningar sporter:'), style={'font-weight': 'bold'}),
        html.P('1. Titta igenom sporterna genom tiderna, vilka sporter har varit OS-sporter?'),
        html.P('2. Finns det några intressanta sporter att analysera?'),
        html.P('3. Dragkamp (Tug-Of-War): Medaljfördelning genom åren?'),
        html.P('4. Speed Skating: Medaljfördelning. Det finns mycket data för sporten.'),
        html.P('5. Tyngdlyftning: Ålder, vikt och längdfördelning över tid? Hade varit intressant att plotta resultaten över tid, men vi har inte den datan.'),
        html.P('6. Basket: Top 10 medaljfördelning alla OS.'),
        html.P('7. Brottning: Top 10 medaljfördelning alla OS.'),
    ], style={'box-shadow': '0px 0px 14px 5px rgba(32,73,179,0.75)', 'text-align': 'center'}),
], fluid=True)