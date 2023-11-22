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
                              title="France medals: Summer and Winter Games.",
                              color_discrete_sequence=['#FFD700', '#C0C0C0', '#CD7F32'])
plt_all_years_medals.update_layout(legend_title_text="Medal", 
                                yaxis_title="Count",
                                xaxis_title="Year")
plt_all_years_medals.update_traces(hovertemplate='Medaljer: %{y}<br>År: %{x}')
# FRA medal Summer OS
plt_summer_medals = px.bar(summer_medals, x="Year", y=["Gold", "Silver", "Bronze"],
                            barmode="stack",
                            title="France medals: Summer Games.",
                            color_discrete_sequence=['#FFD700', '#C0C0C0', '#CD7F32'])
plt_summer_medals.update_layout(legend_title_text="Medal", 
                                yaxis_title="Count",
                                xaxis_title="Year")
plt_summer_medals.update_traces(hovertemplate='Medal: %{y}<br>År: %{x}')
# FRA medal Winter OS 
plt_winter_medals = px.bar(winter_medals, x="Year", y=["Gold", "Silver", "Bronze"],
                            barmode="stack",
                            title="France medals: Winter Games.",
                            color_discrete_sequence=['#FFD700', '#C0C0C0', '#CD7F32'])
plt_winter_medals.update_layout(legend_title_text="Medal", 
                                yaxis_title="Count",
                                xaxis_title="Year")
plt_winter_medals.update_traces(hovertemplate='Medal: %{y}<br>År: %{x}')
# FRA procent/year OS 
plt_fra_andel = px.line(fra_all_medals, x="Year", y="Andel_%")
plt_fra_andel.update_layout(yaxis_title="Procent - %", xaxis_title="Year")
plt_fra_andel.update_traces(line=dict(color='green'))

# Histogram age distribution per Olympic Game:
only_france_df = athlete_events[athlete_events['Team'] == 'France'] # Filter the dataframe to include only rows where the Team is 'France'
only_france_df.sort_values(by=['Year'], inplace=True)
only_france_df.dropna(subset=['Age'], inplace=True)
# Create a histogram of ages over time
histogram_ages_over_time = px.histogram(only_france_df, x='Age', animation_frame='Year', range_x=[10, 90])
# Customize the layout of the histogram
histogram_ages_over_time.update_layout(
    xaxis_title='Age',
    yaxis_title='Count',
    paper_bgcolor="white",
    plot_bgcolor="white",
    font_color="black",
    bargap=0.1,
    yaxis_range=[0, 100]
)
# Load the 'flatly' theme for the Dash application
load_figure_template("flatly")

# Initialize a Dash app with the 'flatly' theme
register_page(__name__,
            path='/page_2',
            title='Frankrike',
            name='Second Page')

layout = dbc.Container([
    html.Br(),
    dbc.Row([
        dbc.Row([
            dbc.Col([
                html.H1("France", className='text-center text-primary mx-3'),
                html.P("Analysis of France's performance in Olympic Games.")
            ], xs=12, sm=11, md=10, lg=9, style={'text-align': 'center'})
        ], justify='center'),
        dbc.Row([
            dbc.Col([
                #html.H1("Drop down", className='text-center text-primary mx-3'),
                html.Br(),
                dcc.Dropdown(
                    options = ["Summer and Winter Games", "Summer Games", "Winter Games"],
                    id="multi_dropdown_1",
                    className='mb-2',
                    value="Summer and Winter Games" 
                )
            ], xs=12, sm=11, md=10, lg=9)
        ], justify="center"),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(id="selected_graph")
            ], xs=12, sm=11, md=10, lg=9),
        ], justify="center"),
    ], style={'border-width': '0px', 'border-radius': '20px', 'box-shadow': '0px 0px 14px 5px rgba(32,73,179,0.75)'}),    
    html.Br(),
    dbc.Row([
        dbc.Row([
            dbc.Col([
                html.H3("Percentage of medals:", style={'text-align':'center','marginTop': '50px'}),
                html.P('Percentage of all medals won by France, per Olympic Game', style={'text-align':'center'}),
                html.Br(),
                dcc.Graph(figure=plt_fra_andel)      
            ], xs=12, sm=11, md=10, lg=9),
        ], justify="center"),
    ], style={'border-width': '0px', 'border-radius': '20px', 'box-shadow': '0px 0px 14px 5px rgba(32,73,179,0.75)'}),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.H3('Age distribution:', style={'text-align':'center','marginTop': '50px'}),
            html.P('Age distribution for France, per Olympic Game', style={'text-align':'center'}),
            dcc.Graph(figure = histogram_ages_over_time)
        ], xs=12, sm=11, md=10, lg=9)
    ], justify="center", style={'margin-bottom': '20px', 'border-width': '0px', 'border-radius': '20px', 'box-shadow': '0px 0px 14px 5px rgba(32,73,179,0.75)'})
], fluid=True)

@callback(
    Output('selected_graph', 'figure'),
    Input('multi_dropdown_1', 'value')
)
def update_graph(selected_value):
    if selected_value == "Summer and Winter Games":
        return plt_all_years_medals
    elif selected_value == "Summer Games":
        return plt_summer_medals
    elif selected_value == "Winter Games":
        return plt_winter_medals