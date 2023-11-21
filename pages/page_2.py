from dash import Dash, html, dcc, callback, Input, Output, register_page
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash_bootstrap_templates import load_figure_template

athlete_events = pd.read_csv('Data/athlete_events.csv')
france = athlete_events[athlete_events["NOC"] == "FRA"] # New DF france 
france.reset_index(drop=True, inplace=True) # set new idx
all_year_medals = france.groupby("Year")["Medal"].value_counts().unstack().fillna(0)
all_year_medals.reset_index(inplace=True)
summer_fra = france[france["Season"] == "Summer"] 
winter_fra = france[france["Season"] == "Winter"]
summer_medals = summer_fra.groupby("Year")["Medal"].value_counts().unstack().fillna(0)
summer_medals.reset_index(inplace=True)
winter_medals = winter_fra.groupby("Year")["Medal"].value_counts().unstack().fillna(0)
winter_medals.reset_index(inplace=True)
all_medals = athlete_events.groupby("Year")["Medal"].count()
all_medals = all_medals.reset_index()
fra_all_medals = france.groupby("Year")["Medal"].count()
fra_all_medals = fra_all_medals.reset_index()
fra_all_medals["Andel_%"] = (fra_all_medals.loc[:, "Medal"] / all_medals.loc[:, "Medal"]) * 100
# FRA all medals
plt_all_years_medals = px.bar(all_year_medals, x="Year", y=["Gold", "Silver", "Bronze"],
                              barmode="stack", 
                              title="Frankrike: OS",
                              color_discrete_sequence=['#FFD700', '#C0C0C0', '#CD7F32'])
plt_all_years_medals.update_layout(legend_title_text="Medal", 
                                yaxis_title="Count",
                                xaxis_title="Year")
plt_all_years_medals.update_traces(hovertemplate='Medaljer: %{y}<br>År: %{x}')
# FRA medal Summer OS
plt_summer_medals = px.bar(summer_medals, x="Year", y=["Gold", "Silver", "Bronze"],
                            barmode="stack",
                            title="Frankrike: Sommar OS",
                            color_discrete_sequence=['#FFD700', '#C0C0C0', '#CD7F32'])
plt_summer_medals.update_layout(legend_title_text="Medal", 
                                yaxis_title="Count",
                                xaxis_title="Year")
plt_summer_medals.update_traces(hovertemplate='Medal: %{y}<br>År: %{x}')
# FRA medal Winter OS 
plt_winter_medals = px.bar(winter_medals, x="Year", y=["Gold", "Silver", "Bronze"],
                            barmode="stack",
                            title="Frankrike: Vinter OS",
                            color_discrete_sequence=['#FFD700', '#C0C0C0', '#CD7F32'])
plt_winter_medals.update_layout(legend_title_text="Medal", 
                                yaxis_title="Count",
                                xaxis_title="Year")
plt_winter_medals.update_traces(hovertemplate='Medal: %{y}<br>År: %{x}')
# FRA procent/year OS 
plt_fra_andel = px.line(fra_all_medals, x="Year", y="Andel_%", title="Frankrike: andel medaljer - OS")
plt_fra_andel.update_layout(yaxis_title="Procent - %", xaxis_title="Year")
plt_fra_andel.update_traces(line=dict(color='green'))
# Load the 'flatly' theme for the Dash application
load_figure_template("flatly")

# Initialize a Dash app with the 'flatly' theme
register_page(__name__, 
            path='/page_2',
            title='Frankrike',
            name='Second Page')

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Frankrike", className='text-center text-primary mx-3'),
            html.Br()
        ], width=12, style={'text-align': 'center'})
    ]),
    dbc.Row([
        dbc.Col([
            #html.H1("Drop down", className='text-center text-primary mx-3'),
            html.Br(),
            dcc.Dropdown(
                options = ["All Seasons", "Summer", "Winter"],
                id="multi_dropdown_1",
                className='mb-2',
                value="All Seasons" 
            )
        ], width=5)
    ], justify="center"),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="selected_graph")
        ], width=9),
    ], justify="center"),
    
    dbc.Row([
        dbc.Col([
            #html.H1("Frankrike: andel medaljer", className='text-center text-primary mx-2'),
            html.Br(),
            dcc.Graph(figure=plt_fra_andel)      
        ], width=9),
    ], justify="center")
], fluid=True)

@callback(
    Output('selected_graph', 'figure'),
    Input('multi_dropdown_1', 'value')
)
def update_graph(selected_value):
    if selected_value == "All Seasons":
        return plt_all_years_medals
    elif selected_value == "Summer":
        return plt_summer_medals
    elif selected_value == "Winter":
        return plt_winter_medals