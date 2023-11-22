from dash import Dash, html, dcc, callback, Input, Output, register_page
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash_bootstrap_templates import load_figure_template

athlete_events = pd.read_csv('Data/athlete_events.csv')
athlete_events.sort_values(by='Year', inplace=True)

# WEIGHTLIFTING:
# Create DataFrame with only sport = weightlifting
weightlifting = athlete_events.query("Sport == 'Weightlifting'") # DF med all weightlifting

#remove NaN's from weight, height and age:
weightlifting = weightlifting.dropna(subset='Weight')
weightlifting = weightlifting.dropna(subset='Height')
weightlifting = weightlifting.dropna(subset='Age')

# removes "Weightlifting " from Event column (shorter text):
weightlifting['Event'] = weightlifting['Event'].str.replace("Weightlifting ","")

# SPEED SKATING:
# Creating a DataFrame containing the events we are interested in:
speed_skating = athlete_events[
    (athlete_events['Event'] == "Speed Skating Men's 1,500 metres") |
    (athlete_events['Event'] == "Speed Skating Men's 500 metres") |
    (athlete_events['Event'] == "Speed Skating Men's 5,000 metres") |
    (athlete_events['Event'] == "Speed Skating Men's 10,000 metres") |
    (athlete_events['Event'] == "Speed Skating Women's 1,000 metres") |
    (athlete_events['Event'] == "Speed Skating Women's 1,500 metres") |
    (athlete_events['Event'] == "Speed Skating Women's 500 metres") |
    (athlete_events['Event'] == "Speed Skating Men's 1,000 metres") |
    (athlete_events['Event'] == "Speed Skating Women's 3,000 metres") |
    (athlete_events['Event'] == "Speed Skating Women's 5,000 metres")
    ]

# dropna NaN's in medal column (är bara intresserad av medaljer):
speed_skating = speed_skating.dropna(axis=0, subset='Medal')
speed_skating

# remove "Speed Skating" som är onödig:
speed_skating['Event'] = speed_skating['Event'].str.replace("Speed Skating ","")

# Creating the main DataFrame:
speed_skating_gb_df = speed_skating.groupby(['Team','Medal','Event','Year'])['Medal'].count().reset_index(name='Medal Count')

# Mask out years with Speed Skating
years = speed_skating_gb_df['Year'].sort_values().unique().tolist()

# BASKETBALL
filter_basket = athlete_events["Sport"] == "Basketball"
basket = athlete_events[filter_basket]
top_basket = basket.groupby("NOC")["Medal"].value_counts().unstack().fillna(0)
top_basket["Tot"] = top_basket.loc[:, "Bronze"] + top_basket.loc[:, "Silver"] + top_basket.loc[:, "Gold"] 
top_basket.sort_values(by="Tot", ascending=False, inplace=True)
top_basket.reset_index(inplace=True)
top_ten_basket = top_basket.loc[:9, :]

plt_top_basket = px.bar(top_ten_basket, x="NOC", y=["Gold", "Silver", "Bronze"],
                        barmode="stack", 
                        color_discrete_sequence=['#FFD700', '#C0C0C0', '#CD7F32'])
plt_top_basket.update_layout(legend_title_text="Medal", 
                                yaxis_title="Count",
                                xaxis_title="Countries")

# WRESTLING
filter_wrest = athlete_events["Sport"] == "Wrestling"
wrestling = athlete_events[filter_wrest]
top_wrestling = wrestling.groupby("NOC")["Medal"].value_counts().unstack().fillna(0)
top_wrestling["Tot"] = top_wrestling.loc[:, "Bronze"] + top_wrestling.loc[:, "Silver"] + top_wrestling.loc[:, "Gold"] 
top_wrestling.sort_values(by="Tot", ascending=False, inplace=True)
top_wrestling.reset_index(inplace=True)
top_ten_wrestling = top_wrestling.loc[:9, :]

plt_top_wrestling = px.bar(top_ten_wrestling, x="NOC", y=["Gold", "Silver", "Bronze"],
                        barmode="stack", 
                        color_discrete_sequence=['#FFD700', '#C0C0C0', '#CD7F32'])
plt_top_wrestling.update_layout(legend_title_text="Medal", 
                                yaxis_title="Count",
                                xaxis_title="Countries")

# TUG-OF-WAR
tug_of_war = athlete_events[athlete_events['Sport'] == "Tug-Of-War"]
tow_year = tug_of_war.groupby(['Year','Team'])
my_tow_df = tow_year['Medal'].value_counts()
my_tow_df = my_tow_df.reset_index()
tow_fig = px.bar(my_tow_df, x='Year',
    y='count',
    color='Medal',
    text='Year',
    hover_data='Team',
    hover_name='Team',
    color_discrete_sequence=['#FFD700', '#C0C0C0', '#CD7F32'])

#========================================================
# Load the 'flatly' theme for the Dash application
load_figure_template("flatly")

# Initialize a Dash app with the 'flatly' theme
register_page(__name__, 
            path='/page_3',
            title='Sportanalys',
            name='Sportanalys')

layout = dbc.Container([
    html.Br(),
    dbc.Row([
        dbc.Row([
            dbc.Col([
                html.H1("Speed Skating", className='text-center text-primary mx-3'),
                html.P("Number of medals per Team, for selcted event and year interval."),
                html.Br()
            ], xs=12, sm=11, md=10, lg=9, style={'text-align': 'center'}),
        ], justify='center'),
        dbc.Row([
            dbc.Col([
                html.P('Select event:'),
                dcc.Dropdown(
                    id="multi_dropdown",
                    multi=True,
                    searchable=False, 
                    className='mb-2',
                    placeholder='Select event',
                    options=[event for event in speed_skating_gb_df['Event'].unique()],
                    value=["Men's 1,500 metres"]
                ),
            ], xs=12, sm=11, md=10, lg=9),
        ], justify='center'),
        dbc.Row([
            dbc.Col([
                html.Br(),
                html.P("Select year interval:"),
                dcc.RangeSlider(
                    min=min(years),
                    max=max(years),
                    step=1,
                    marks=None,
                    value=[1896, 2016],
                    id="RangeSlider",
                ),
            ], xs=12, sm=11, md=10, lg=9),
        ], justify='center'),
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id='skate_graph',
                    config={'staticPlot':True},
                    figure={}
                ),
            ], xs=12, sm=11, md=10, lg=9),
        ], justify='center'),
    ], style={'border-width': '0px', 'border-radius': '20px', 'box-shadow': '0px 0px 14px 5px rgba(32,73,179,0.75)'}),
    html.Br(),
    dbc.Row([
        dbc.Row([
            dbc.Col([
                html.H1("Weightlifting", className='text-center text-primary mx-3'),
                html.P("Age, Weight and Height Analysis of all participants, over time.",style={'text-align': 'center'}),
                html.Br(),
                html.P("Select event:"),
                dcc.RadioItems(
                    options=[event for event in weightlifting['Event'].unique()],
                    id="weightlifting-event",
                    inline=True,
                    value="Women's Super-Heavyweight",
                    style={'margin': '30px'}
                ),
            ], xs=12, sm=11, md=10, lg=9),
        ], justify='center'),
        dbc.Row([
            dbc.Col([
                html.Br(),
                html.P("Select attribute:"),
                dcc.RadioItems(
                    ['Age','Weight','Height'],
                    id="weightlifting-attr",
                    inline=True,
                    value='Age',
                    style={'margin': '30px'}
                ),
            ], xs=12, sm=11, md=10, lg=9,),
        ], justify='center'),
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id='weightlifting-graph',
                    config={'staticPlot':True},
                    figure={}
                ),
            ], xs=12, sm=11, md=10, lg=9),
        ], justify='center'),
    ], style={'border-width': '0px', 'border-radius': '20px', 'box-shadow': '0px 0px 14px 5px rgba(32,73,179,0.75)'}),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                html.H1('Basketball', className='text-center text-primary mx-3'),
                html.P('Top-10 countries, all Olympic Games.'),
                dcc.Graph(
                    figure = plt_top_basket
                ),
            ], style={'border-width': '0px', 'border-radius': '20px', 'box-shadow': '0px 0px 14px 5px rgba(32,73,179,0.75)'}),
            html.Br(),
            dbc.Row([
                html.H1('Wrestling', className='text-center text-primary mx-3'),
                html.P('Top 10 countries, all Olympic Games.'),
                dcc.Graph(
                    figure = plt_top_wrestling
                ),
            ], style={'border-width': '0px', 'border-radius': '20px', 'box-shadow': '0px 0px 14px 5px rgba(32,73,179,0.75)'}),
            html.Br(),
            dbc.Row([
                html.H1('Tug-Of-War', className='text-center text-primary mx-3'),
                html.P('Awarded medals. Hover to read Team name.'),
                dcc.Graph(
                    figure = tow_fig
                ),
            ], style={'border-width': '0px', 'border-radius': '20px', 'box-shadow': '0px 0px 14px 5px rgba(32,73,179,0.75)'}),
        ], xs=12, sm=11, md=10, lg=9, style={'text-align': 'center'})
    ], justify='center'),
], fluid=True)


@callback(
    Output("skate_graph", "figure"),
    Input("RangeSlider", "value"),
    Input("multi_dropdown", "value")
)

def update_multidropdown(year, events):
    if events is None: events = []
    if year is None: year = [1896, 1922]
    df = speed_skating_gb_df[(speed_skating_gb_df['Event'].isin(events)) & (speed_skating_gb_df['Year'] >= year[0]) & (speed_skating_gb_df['Year'] <= year[1])]
    fig_speed_skating = px.bar(df,
                x='Team',
                y='Medal Count',
                hover_name='Event',
                hover_data='Event',
                color='Medal',
                color_discrete_sequence=['#CD7F32', '#FFD700', '#C0C0C0'],
                title=f'Speed Skating medals, between {year[0]} and {year[1]}, per Team:')
    fig_speed_skating.update_layout(title={'xanchor': 'center','x': 0.5,'yanchor': 'top','font': {'size': 20}})

    return fig_speed_skating
        
@callback(
    Output('weightlifting-graph','figure'),
    Input('weightlifting-event','value'),
    Input('weightlifting-attr', 'value')
)

def update_weightlifting(event, attr):
    event = [event] #måste göra om str till list
    if event is None: event = ["Women's Super-Heavyweight"]
    if attr is None: attr = []
    df = weightlifting[(weightlifting['Event'].isin(event))]
    fig_weightlifting = px.box(
        df,                               
        x='Year',
        y=attr,
        title=f'{attr} for {event[0]}:')
    
    fig_weightlifting.update_layout(title={'xanchor': 'center','x': 0.5,'yanchor': 'top','font': {'size': 20}})

    return fig_weightlifting