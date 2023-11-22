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
        html.H3('Grupp Frankrike:')
    ]),
    dbc.Row([
        html.P('Medlemmar: Asajad, Arsen, Daniel.', style={'margin':'30px'})
    ]),
    dbc.Row([
        html.H3('Frågeställningar Frankrike:')
    ]),
    dbc.Row([
        html.P('1. Vilken eller vilka sporter har Frankrike varit mest framgångsrikt i?'),
        html.P('2. Har Frankrike varit mest framgångsrikt i sommar eller vinter OS?'),
        html.P('3. Finns det någon tid i historien som kan sägas vara Frankrikes storhetstid i OS?'),
        html.P('4. Vilket var Frankrikes bästa OS?'),
        html.P('5. Vilka sporter har Frankrike varit sämst i? Finns det någon sport de inte fått medalj i, tex?'),
        html.P('6. Hur ser åldersfördelningen ut för Frankrike genom åren?'),
    ]),
    dbc.Row([
        html.H3('Frågeställningar sporter:')
    ]),
    dbc.Row([
        html.P('1. Titta igenom sporterna genom tiderna, vilka sporter har varit OS-sporter?'),
        html.P('2. Finns det några gamla intressanta sporter att analysera? Eller sporter som vi är intresserade av?'),
        html.P('3. Dragkamp (Tug-Of-War): Medaljfördelning genom åren?'),
        html.P('4. Speed Skating: Medaljfördelning. Det finns mycket data för sporten.'),
        html.P('5. Tyngdlyftning: Ålder, vikt och längdfördelning över tid? Hade varit intressant att plotta resultaten över tid, men vi har inte den datan.'),
        html.P('6. Basket: Top 10 medaljfördelning alla OS.'),
        html.P('7. Brottning: Top 10 medaljfördelning alla OS.'),
    ]),
    dbc.Row([
        html.H2('Antalet länder som har deltagit:'),
        html.H3(athlete_events['NOC'].nunique())
    ]),

    dbc.Row([
        html.H2('Länder:'),
        html.H3(list(athlete_events['NOC'].unique())),
    ]),
], fluid=True)