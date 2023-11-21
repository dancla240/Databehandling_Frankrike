from dash import Dash, html, dcc, callback, Input, Output, register_page
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
            path='/page_1',
            title='Page 1',
            name='Page 1')

# Define the layout of the app using the Dash Bootstrap Components (dbc)
layout = dbc.Container([
    # First Row: Filters for Year, Nation Code, and Sport and also the Title
    dbc.Row([
        dbc.Col([
            dbc.Row([
                html.H1('Olympic Games', style={'fontSize': '30px', 'border-width': '0px', 'border-style': 'solid', 'border-radius': '20px', 'box-shadow': '0px 0px 14px 5px rgba(32,73,179,0.75)', 'text-align': 'center', 'padding-top': '10px', 'padding-bottom': '10px'}),
            ], justify='center', style={}),
            dbc.Row([
                dbc.Col([
                    html.H3('Year', style={'fontSize': '24px'}, className="mt-2"),
                    dcc.Dropdown(
                        id='year_dropdown',
                        options=[{'label': i, 'value': i} for i in athlete_events['Year'].unique()],
                        value=None,
                        style={'width': '95%'}
                    ),
                ], width = 3, style={'border-color': 'black', 'border-width': '0px', 'border-style': 'solid', 'border-radius': '20px', 'box-shadow': '0px 0px 14px 5px rgba(32,73,179,0.75)', 'text-align': 'center', 'margin-top': '10px'}),
                dbc.Col([
                    html.H3('Nation Code', style={'fontSize': '24px'}, className="mt-2"),
                    dcc.Dropdown(
                        id='country_dropdown',
                        options=[{'label': i, 'value': i} for i in athlete_events['NOC'].unique()],
                        value=None,
                        style={'width': '95%'}
                    ),
                ], width = 3, style={'border-color': 'black', 'border-width': '0px', 'border-style': 'solid', 'border-radius': '20px', 'box-shadow': '0px 0px 14px 5px rgba(32,73,179,0.75)', 'text-align': 'center', 'margin-top': '10px'}),
                dbc.Col([
                    html.Div(
                        [html.H3('Sport', style={'fontSize': '24px'}, className="mt-2"),
                        dcc.Dropdown(
                            id='sport_dropdown',
                            options=[{'label': i, 'value': i} for i in athlete_events['Sport'].unique()],
                            value=None,
                            style={'width': '95%'}
                        )],
                    ),
                ], width=3, style={'border-color': 'black', 'border-width': '0px', 'border-style': 'solid', 'border-radius': '20px', 'box-shadow': '0px 0px 14px 5px rgba(32,73,179,0.75)', 'text-align': 'center', 'margin-top': '10px'}),
                dbc.Col([
                    html.Div(
                        [html.H3('No. of competitors:', style={'fontSize': '20px', }),
                        html.H3(id="no_competitors")],
                        style={'border-color': 'black', 'border-width': '0px', 'border-style': 'solid', 'border-radius': '20px', 'box-shadow': '0px 0px 14px 5px rgba(32,73,179,0.75)', 'text-align': 'center'}
                    ),
                    html.Div(
                        [html.H3('No. of Medals:', style={'fontSize': '20px'}),
                        html.H3(id="no_medals")],
                        style={'border-color': 'black', 'border-width': '0px', 'border-style': 'solid', 'border-radius': '20px', 'box-shadow': '0px 0px 14px 5px rgba(32,73,179,0.75)', 'text-align': 'center'}
                    )
                ], width = 3),
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='pie_chart_competitor_gender', style={'margin-top': '20px'}),
                ], xs=11, sm=11, md=10, lg=6, style={'border-color': 'black', 'border-width': '0px', 'border-style': 'solid', 'border-radius': '20px', 'box-shadow': '0px 0px 14px 5px rgba(32,73,179,0.75)'}),

                dbc.Col([
                    dcc.Graph(id="pie_chart_medal_gender", style={'margin-top': '20px'}),
                ], xs=11, sm=11, md=10, lg=6, style={'border-color': 'black', 'border-width': '0px', 'border-style': 'solid', 'border-radius': '20px', 'box-shadow': '0px 0px 14px 5px rgba(32,73,179,0.75)'}),
            ])
        ], xs=11, sm=11, md=10, lg=6),
        # Third Column: Medal Breakdown by Top 10 Sports & Type
        dbc.Col([
            html.H3('Medal Breakdown By Top 10 Sports & Type', style={'fontSize': '16px'}),
            dcc.Graph(id='medal_breakdown_sport')
        ], xs=11, sm=11, md=10, lg=3, style={'border-color': 'black', 'border-width': '0px', 'border-style': 'solid', 'border-radius': '20px', 'box-shadow': '0px 0px 14px 5px rgba(32,73,179,0.75)'}),

        # Fourth Column: Medal Breakdown By Top 10 Athlete & Type
        dbc.Col([
            html.H3('Medal breakdown By Top 10 Athlete & Type', style={'fontSize': '16px'}),
            dcc.Graph(id='medal_breakdown_athlete')
        ], xs=11, sm=11, md=10, lg=3, style={'border-color': 'black', 'border-width': '0px', 'border-style': 'solid', 'border-radius': '20px', 'box-shadow': '0px 0px 14px 5px rgba(32,73,179,0.75)'}),    
    ], justify='center', style={'margin-top': '20px'}),

], fluid=True)


# Define a callback function that updates multiple components in the app based on user inputs
@callback(
    Output('no_competitors', 'children'),
    Output('no_medals', 'children'),
    Output('medal_breakdown_sport', 'figure'),
    Output('medal_breakdown_athlete', 'figure'),
    Output('pie_chart_competitor_gender', 'figure'),
    Output('pie_chart_medal_gender', 'figure'),
    Input('year_dropdown', 'value'),
    Input('country_dropdown', 'value'),
    Input('sport_dropdown', 'value'),
)

def update_graph(year, country, sport):
    # If no specific filters are applied, provide overall statistics
    if year is None and country is None and sport is None:
        # Calculate the total number of unique competitors
        no_of_competitors = athlete_events['Name'].nunique()

        # Calculate the total number of medals
        no_of_medals = athlete_events['Medal'].count()

        # Medal breakdown by sport for the top 10 sports with the most medals
        top_10_sports_medal_breakdown = medal_breakdown_sports_none_selected()

        # Create a horizontal stacked bar chart for medal breakdown by sport
        fig_sports = px.bar(top_10_sports_medal_breakdown, y='Sport', x='Count', color='Medal', barmode='stack', orientation='h')
        set_medal_colors(fig_sports)

        # Medal breakdown by athlete for the top 10 athletes with the most medals
        top_10_athletes_medal_breakdown = medal_breakdown_athletes_none_selected()

        # Create a horizontal stacked bar chart for medal breakdown by athlete
        fig_athletes = px.bar(top_10_athletes_medal_breakdown, y='Name', x='Count', color='Medal', barmode='stack', orientation='h')
        set_medal_colors(fig_athletes)

        # Create a pie chart for competitors by gender
        unique_competitors = athlete_events[['Name', 'Sex']].drop_duplicates()
        sex_counts = unique_competitors['Sex'].value_counts()
        pie_chart_competitors = px.pie(names=['Women', 'Men'], values=sex_counts.values, title="Competitors by gender")
        pie_chart_competitors.update_traces(textposition='inside', textinfo='percent+label')
        pie_chart_competitors.update_layout(showlegend=False)

        # Create a pie chart for the proportion of medals won by women and men
        medal_gender_counts = athlete_events.groupby(['Sex', 'Medal'])['Medal'].count().reset_index(name='Count')
        women_counts = medal_gender_counts[medal_gender_counts['Sex'] == 'F']
        men_counts = medal_gender_counts[medal_gender_counts['Sex'] == 'M']
        pie_chart_medals = px.pie(names=['Women', 'Men'], values=[women_counts['Count'].sum(), men_counts['Count'].sum()], title='Proportion of Medals Won by Gender')
        pie_chart_medals.update_traces(textposition='inside', textinfo='percent+label')
        pie_chart_medals.update_layout(showlegend=False)

    # Check if only the 'sport' filter is applied (year and country are None)
    elif year is None and country is None:
        # Calculate the number of competitors for the selected sport
        no_of_competitors = athlete_events.groupby('Sport').get_group(sport)['Name'].nunique()

        # Calculate the total number of medals for the selected sport
        no_of_medals = athlete_events.groupby('Sport').get_group(sport)['Medal'].count()

        # Medal breakdown by sport for the selected sport
        top_10_sports_medal_breakdown = medal_breakdown_sports_single_selected('Sport', sport)

        # Create a horizontal stacked bar chart for medal breakdown by sport
        fig_sports = px.bar(top_10_sports_medal_breakdown, y='Sport', x='Count', color='Medal', barmode='stack', orientation='h')
        set_medal_colors(fig_sports)

        # Medal breakdown by athlete for the selected sport
        top_10_athletes_medal_breakdown = medal_breakdown_athletes_single_selected('Sport', sport)

        # Create a horizontal stacked bar chart for medal breakdown by athlete
        fig_athletes = px.bar(top_10_athletes_medal_breakdown, y='Name', x='Count', color='Medal', barmode='stack', orientation='h')
        set_medal_colors(fig_athletes)

        # Create a pie chart for competitors by gender for the selected sport
        unique_competitors = athlete_events[['Name', 'Sex', 'Sport']].drop_duplicates().groupby('Sport').get_group(sport)
        sex_counts = unique_competitors['Sex'].value_counts()
        pie_chart_competitors = px.pie(names=['Women', 'Men'], values=sex_counts.values, title="Competitors by gender", width=350, height=350)
        pie_chart_competitors.update_traces(textposition='inside', textinfo='percent+label')
        pie_chart_competitors.update_layout(showlegend=False)

        # Medal breakdown by gender for the selected sport
        medal_gender_counts = athlete_events[['Sex', 'Sport', 'Medal']].groupby(['Sport']).get_group(sport).dropna()

        # Filter the counts for women and men
        medal_counts_men = medal_gender_counts[medal_gender_counts['Sex'] == 'M'].value_counts().sum()
        medal_counts_women = medal_gender_counts[medal_gender_counts['Sex'] == 'F'].value_counts().sum()

        # Create a pie chart for the proportion of medals won by women and men
        pie_chart_medals = px.pie(names=['Women', 'Men'], values=[medal_counts_women, medal_counts_men], title='Proportion of Medals Won by Gender', width=350, height=350)

        # Show the percentage labels on the pie chart
        pie_chart_medals.update_traces(textposition='inside', textinfo='percent+label')
        pie_chart_medals.update_layout(showlegend=False)

    # Check if only the 'country' filter is applied (year and sport are None)
    elif year is None and sport is None:
        # Calculate the number of competitors for the selected country
        no_of_competitors = athlete_events.groupby('NOC').get_group(country)['Name'].nunique()

        # Calculate the total number of medals for the selected country
        no_of_medals = athlete_events.groupby('NOC').get_group(country)['Medal'].count()

        # Medal breakdown by sport for the selected sport
        top_10_sports_medal_breakdown = medal_breakdown_sports_single_selected('NOC', country)

        # Create a horizontal stacked bar chart for medal breakdown by sport
        fig_sports = px.bar(top_10_sports_medal_breakdown, y='Sport', x='Count', color='Medal', barmode='stack', orientation='h')
        set_medal_colors(fig_sports)

        # Medal breakdown by athlete for the selected country
        top_10_athletes_medal_breakdown = medal_breakdown_athletes_single_selected('NOC', country)

        # Create a horizontal stacked bar chart for medal breakdown by athlete
        fig_athletes = px.bar(top_10_athletes_medal_breakdown, y='Name', x='Count', color='Medal', barmode='stack', orientation='h')
        set_medal_colors(fig_athletes)

        # Create a pie chart for competitors by gender for the selected country
        unique_competitors = athlete_events[['Name', 'Sex', 'NOC']].drop_duplicates().groupby('NOC').get_group(country)
        sex_counts = unique_competitors['Sex'].value_counts()
        pie_chart_competitors = px.pie(names=['Women', 'Men'], values=sex_counts.values, title="Competitors by gender", width=350, height=350)
        pie_chart_competitors.update_traces(textposition='inside', textinfo='percent+label')
        pie_chart_competitors.update_layout(showlegend=False)

        # Medal breakdown by gender for the selected country
        medal_gender_counts = athlete_events[['Sex', 'NOC', 'Medal']].groupby(['NOC']).get_group(country).dropna()

        # Filter the counts for women and men
        medal_counts_men = medal_gender_counts[medal_gender_counts['Sex'] == 'M'].value_counts().sum()
        medal_counts_women = medal_gender_counts[medal_gender_counts['Sex'] == 'F'].value_counts().sum()

        # Create a pie chart for the proportion of medals won by women and men
        pie_chart_medals = px.pie(names=['Women', 'Men'], values=[medal_counts_women, medal_counts_men], title='Proportion of Medals Won by Gender', width=350, height=350)

        # Show the percentage labels on the pie chart
        pie_chart_medals.update_traces(textposition='inside', textinfo='percent+label')
        pie_chart_medals.update_layout(showlegend=False)

    # Check if only the 'year' filter is applied (country and sport are None)
    elif country is None and sport is None:
        # Calculate the number of competitors for the selected year
        no_of_competitors = athlete_events.groupby('Year').get_group(year)['Name'].nunique()

        # Calculate the total number of medals for the selected year
        no_of_medals = athlete_events.groupby('Year').get_group(year)['Medal'].count()

        # Medal breakdown by sport for the selected sport
        top_10_sports_medal_breakdown = medal_breakdown_sports_single_selected('Year', year)

        # Create a horizontal stacked bar chart for medal breakdown by sport
        fig_sports = px.bar(top_10_sports_medal_breakdown, y='Sport', x='Count', color='Medal', barmode='stack', orientation='h')
        set_medal_colors(fig_sports)

        # Medal breakdown by athlete for the selected year
        top_10_athletes_medal_breakdown = medal_breakdown_athletes_single_selected('Year', year)

        # Create a horizontal stacked bar chart for medal breakdown by athlete
        fig_athletes = px.bar(top_10_athletes_medal_breakdown, y='Name', x='Count', color='Medal', barmode='stack', orientation='h')
        set_medal_colors(fig_athletes)

        # Create a pie chart for competitors by gender for the selected year
        unique_competitors = athlete_events[['Name', 'Sex', 'Year']].drop_duplicates().groupby('Year').get_group(year)
        sex_counts = unique_competitors['Sex'].value_counts()
        pie_chart_competitors = px.pie(names=['Women', 'Men'], values=sex_counts.values, title="Competitors by gender", width=350, height=350)
        pie_chart_competitors.update_traces(textposition='inside', textinfo='percent+label')
        pie_chart_competitors.update_layout(showlegend=False)

        # Medal breakdown by gender for the selected year
        medal_gender_counts = athlete_events[['Sex', 'Year', 'Medal']].groupby(['Year']).get_group(year).dropna()

        # Filter the counts for women and men
        medal_counts_men = medal_gender_counts[medal_gender_counts['Sex'] == 'M'].value_counts().sum()
        medal_counts_women = medal_gender_counts[medal_gender_counts['Sex'] == 'F'].value_counts().sum()

        # Create a pie chart for the proportion of medals won by women and men
        pie_chart_medals = px.pie(names=['Women', 'Men'], values=[medal_counts_women, medal_counts_men], title='Proportion of Medals Won by Gender', width=350, height=350)

        # Show the percentage labels on the pie chart
        pie_chart_medals.update_traces(textposition='inside', textinfo='percent+label')
        pie_chart_medals.update_layout(showlegend=False)

    # Check if only the 'country' filter is None (year and sport are applied)
    elif country is None:
        # Calculate the number of competitors for the selected year and sport
        no_of_competitors = athlete_events.groupby('Year').get_group(year)['Name'].nunique()

        # Calculate the total number of medals for the selected year and sport
        no_of_medals = athlete_events.groupby('Year').get_group(year)['Medal'].count()

        medal_top_10_sports = medal_breakdown_sports_double_selected('Sport', sport, 'Year', year)
        # Create a horizontal stacked bar chart for medal breakdown by athlete for the selected country and sport
        fig_sports = px.bar(medal_top_10_sports, y=medal_top_10_sports.index, x=['Bronze', 'Silver', 'Gold'], barmode='stack', orientation='h')
        set_medal_colors(fig_sports)

        # Medal breakdown by athlete for the selected year and sport
        top_10_athletes_medal_breakdown = medal_breakdown_athletes_double_selected('Sport', sport, 'Year', year)

        # Create a horizontal stacked bar chart for medal breakdown by athlete
        fig_athletes = px.bar(top_10_athletes_medal_breakdown, y='Name', x='Count', color='Medal', barmode='stack', orientation='h')
        set_medal_colors(fig_athletes)

        # Create a pie chart for competitors by gender for the selected year and sport
        unique_competitors = athlete_events[['Name', 'Sex', 'Sport', 'Year']].drop_duplicates().groupby('Sport').get_group(sport).groupby('Year').get_group(year)
        sex_counts = unique_competitors['Sex'].value_counts()
        pie_chart_competitors = px.pie(names=['Women', 'Men'], values=sex_counts.values, title="Competitors by gender", width=350, height=350)
        pie_chart_competitors.update_traces(textposition='inside', textinfo='percent+label')
        pie_chart_competitors.update_layout(showlegend=False)

        # Medal breakdown by gender for the selected year and sport
        medal_gender_counts = athlete_events[['Sex', 'Sport', 'Medal', 'Year']].groupby('Sport').get_group(sport).groupby('Year').get_group(year).dropna()

        # Filter the counts for women and men
        medal_counts_men = medal_gender_counts[medal_gender_counts['Sex'] == 'M'].value_counts().sum()
        medal_counts_women = medal_gender_counts[medal_gender_counts['Sex'] == 'F'].value_counts().sum()

        # Create a pie chart for the proportion of medals won by women and men
        pie_chart_medals = px.pie(names=['Women', 'Men'], values=[medal_counts_women, medal_counts_men], title='Proportion of Medals Won by Gender', width=350, height=350)

        # Show the percentage labels on the pie chart
        pie_chart_medals.update_traces(textposition='inside', textinfo='percent+label')
        pie_chart_medals.update_layout(showlegend=False)

    # Check if only the 'sport' filter is None (country and year are applied)
    elif sport is None:
        # Calculate the number of competitors for the selected country and year
        no_of_competitors = athlete_events.groupby('NOC').get_group(country).groupby('Year').get_group(year)['Name'].nunique()

        # Calculate the total number of medals for the selected country and year
        no_of_medals = athlete_events.groupby('NOC').get_group(country).groupby('Year').get_group(year)['Medal'].count()

        medal_top_10_sports = medal_breakdown_sports_double_selected('NOC', country, 'Year', year)
        # Create a horizontal stacked bar chart for medal breakdown by athlete for the selected country and sport
        fig_sports = px.bar(medal_top_10_sports, y=medal_top_10_sports.index, x=['Bronze', 'Silver', 'Gold'], barmode='stack', orientation='h')
        set_medal_colors(fig_sports)

        top_10_athletes_medal_breakdown = medal_breakdown_athletes_double_selected('NOC', country, 'Year', year)

        # Create a horizontal stacked bar chart for medal breakdown by athlete for the selected country and year
        fig_athletes = px.bar(top_10_athletes_medal_breakdown, y='Name', x='Count', color='Medal', barmode='stack', orientation='h')
        set_medal_colors(fig_athletes)

        # Create a pie chart for competitors by gender for the selected country and year
        unique_competitors = athlete_events[['Name', 'Sex', 'NOC', 'Year']].drop_duplicates().groupby('NOC').get_group(country).groupby('Year').get_group(year)
        sex_counts = unique_competitors['Sex'].value_counts()
        pie_chart_competitors = px.pie(names=['Women', 'Men'], values=sex_counts.values, title="Competitors by gender", width=350, height=350)
        pie_chart_competitors.update_traces(textposition='inside', textinfo='percent+label')
        pie_chart_competitors.update_layout(showlegend=False)

        # Medal breakdown by gender for the selected country and year
        medal_gender_counts = athlete_events[['Sex', 'NOC', 'Medal', 'Year']].groupby('NOC').get_group(country).groupby('Year').get_group(year).dropna()

        # Filter the counts for women and men
        medal_counts_men = medal_gender_counts[medal_gender_counts['Sex'] == 'M'].value_counts().sum()
        medal_counts_women = medal_gender_counts[medal_gender_counts['Sex'] == 'F'].value_counts().sum()

        # Create a pie chart for the proportion of medals won by women and men for the selected country and year
        pie_chart_medals = px.pie(names=['Women', 'Men'], values=[medal_counts_women, medal_counts_men], title='Proportion of Medals Won by Gender', width=350, height=350)

        # Show the percentage labels on the pie chart
        pie_chart_medals.update_traces(textposition='inside', textinfo='percent+label')
        pie_chart_medals.update_layout(showlegend=False)

    # Check if only the 'year' filter is None (country and sport are applied)
    elif year is None:
        # Calculate the number of competitors for the selected country and sport
        no_of_competitors = athlete_events.groupby('NOC').get_group(country)['Name'].nunique()

        # Calculate the total number of medals for the selected country and sport
        no_of_medals = athlete_events.groupby('NOC').get_group(country)['Medal'].count()

        medal_top_10_sports = medal_breakdown_sports_double_selected('NOC', country, 'Sport', sport)
        fig_sports = px.bar(medal_top_10_sports, y=medal_top_10_sports.index, x=['Bronze', 'Silver', 'Gold'], barmode='stack', orientation='h')
        set_medal_colors(fig_sports)

        top_10_athletes_medal_breakdown = medal_breakdown_athletes_double_selected('Sport', sport, 'NOC', country)

        # Create a horizontal stacked bar chart for medal breakdown by athlete for the selected country and sport
        fig_athletes = px.bar(top_10_athletes_medal_breakdown, y='Name', x='Count', color='Medal', barmode='stack', orientation='h')
        set_medal_colors(fig_athletes)

        # Create a pie chart for competitors by gender for the selected country and sport
        unique_competitors = athlete_events[['Name', 'Sex', 'NOC', 'Sport']].drop_duplicates().groupby('NOC').get_group(country).groupby('Sport').get_group(sport)
        sex_counts = unique_competitors['Sex'].value_counts()
        pie_chart_competitors = px.pie(names=['Women', 'Men'], values=sex_counts.values, title="Competitors by gender", width=350, height=350)
        pie_chart_competitors.update_traces(textposition='inside', textinfo='percent+label')
        pie_chart_competitors.update_layout(showlegend=False)

        # Medal breakdown by gender for the selected country and sport
        medal_gender_counts = athlete_events[['Sex', 'Sport', 'Medal', 'NOC']].groupby('Sport').get_group(sport).groupby('NOC').get_group(country).dropna()

        # Filter the counts for women and men
        medal_counts_men = medal_gender_counts[medal_gender_counts['Sex'] == 'M'].value_counts().sum()
        medal_counts_women = medal_gender_counts[medal_gender_counts['Sex'] == 'F'].value_counts().sum()

        # Create a pie chart for the proportion of medals won by women and men for the selected country and sport
        pie_chart_medals = px.pie(names=['Women', 'Men'], values=[medal_counts_women, medal_counts_men], title='Proportion of Medals Won by Gender', width=350, height=350)

        # Show the percentage labels on the pie chart
        pie_chart_medals.update_traces(textposition='inside', textinfo='percent+label')
        pie_chart_medals.update_layout(showlegend=False)

    # Check if all filters are applied
    else:
        # Calculate the number of competitors for the selected year, country and sport
        no_of_competitors = athlete_events[(athlete_events['Year'] == year) & (athlete_events['NOC'] == country)]['Name'].nunique()

        # Calculate the total number of medals for the selected year, country and sport
        no_of_medals = athlete_events[(athlete_events['Year'] == year) & (athlete_events['NOC'] == country) & (athlete_events['Sport'] == sport)]['Medal'].count()


        medal_top_10_sports = medal_breakdown_sports_triple_selected('NOC', country, 'Sport', sport, 'Year', year)

        # Create a horizontal stacked bar chart for medal breakdown by athlete for the selected country and sport
        fig_sports = px.bar(medal_top_10_sports, y=medal_top_10_sports.index, x=['Bronze', 'Silver', 'Gold'], barmode='stack', orientation='h')
        set_medal_colors(fig_sports)

        top_10_athletes_medal_breakdown = medal_breakdown_athletes_triple_selected('NOC', country, 'Year', year, 'Sport', sport)

        # Create a horizontal stacked bar chart for medal breakdown by athlete for the selected year, country and sport
        fig_athletes = px.bar(top_10_athletes_medal_breakdown, y='Name', x='Count', color='Medal', barmode='stack', orientation='h')
        set_medal_colors(fig_athletes)

        # Create a pie chart for competitors by gender for the selected year, country, and sport
        unique_competitors = athlete_events[['Name', 'Sex', 'NOC', 'Year', 'Sport']].drop_duplicates().groupby('NOC').get_group(country).groupby('Year').get_group(year).groupby('Sport').get_group(sport)
        sex_counts = unique_competitors['Sex'].value_counts()
        pie_chart_competitors = px.pie(names=['Women', 'Men'], values=sex_counts.values, title="Competitors by gender", width=350, height=350)
        pie_chart_competitors.update_traces(textposition='inside', textinfo='percent+label')
        pie_chart_competitors.update_layout(showlegend=False)

        # Medal breakdown by gender for the selected year, country, and sport
        medal_gender_counts = athlete_events[['Sex', 'Sport', 'Medal', 'Year', 'NOC']].groupby('Sport').get_group(sport).groupby('Year').get_group(year).groupby('NOC').get_group(country).dropna()

        # Filter the counts for women and men
        medal_counts_men = medal_gender_counts[medal_gender_counts['Sex'] == 'M'].value_counts().sum()
        medal_counts_women = medal_gender_counts[medal_gender_counts['Sex'] == 'F'].value_counts().sum()

        # Create a pie chart for the proportion of medals won by women and men for the selected year, country and sport
        pie_chart_medals = px.pie(names=['Women', 'Men'], values=[medal_counts_women, medal_counts_men], title='Proportion of Medals Won by Gender', width=350, height=350)

        # Show the percentage labels on the pie chart
        pie_chart_medals.update_traces(textposition='inside', textinfo='percent+label')
        pie_chart_medals.update_layout(showlegend=False)

    # Return the calculated values and figures
    return no_of_competitors, no_of_medals, fig_sports, fig_athletes, pie_chart_competitors, pie_chart_medals

def set_medal_colors(figure):
    figure.update_traces(marker_color='#CD7F32', selector=dict(name='Bronze'))
    figure.update_traces(marker_color='silver', selector=dict(name='Silver'))
    figure.update_traces(marker_color='gold', selector=dict(name='Gold'))

def medal_breakdown_sports_none_selected():
    medal_breakdown = athlete_events.groupby(['Sport', 'Medal'])['Medal'].count().reset_index(name='Count')
    top_10_sports = medal_breakdown.groupby('Sport')['Count'].sum().nlargest(10).index
    top_10_sports_medal_breakdown = medal_breakdown[medal_breakdown['Sport'].isin(top_10_sports)]
    top_10_sports_medal_breakdown['Total'] = top_10_sports_medal_breakdown.groupby('Sport')['Count'].transform('sum')
    top_10_sports_medal_breakdown.sort_values(by='Total', ascending=True, inplace=True)

    return top_10_sports_medal_breakdown

def medal_breakdown_sports_single_selected(arg1, arg2):
    medal_breakdown = athlete_events[athlete_events[arg1] == arg2].groupby(['Sport', 'Medal'])['Medal'].count().reset_index(name='Count')
    top_10_sports = medal_breakdown.groupby('Sport')['Count'].sum().nlargest(10).index
    top_10_sports_medal_breakdown = medal_breakdown[medal_breakdown['Sport'].isin(top_10_sports)]
    top_10_sports_medal_breakdown['Total'] = top_10_sports_medal_breakdown.groupby('Sport')['Count'].transform('sum')
    top_10_sports_medal_breakdown.sort_values(by='Total', ascending=True, inplace=True)
    return top_10_sports_medal_breakdown

def medal_breakdown_sports_double_selected(arg1, arg2, arg3, arg4):
    filtered_data = athlete_events[(athlete_events[arg1] == arg2) & (athlete_events[arg3] == arg4)]
    medal_counts = filtered_data.pivot_table(index='Sport', columns='Medal', values='ID', aggfunc='count', fill_value=0)
    medal_counts.columns = ['Bronze', 'Gold', 'Silver']
    medal_top_10_sports = medal_counts.head(10)
    medal_top_10_sports['Total'] = medal_top_10_sports.sum(axis=1)
    medal_top_10_sports.sort_values(by='Total', inplace=True, ascending=True)
    return medal_top_10_sports

def medal_breakdown_sports_triple_selected(arg1, arg2, arg3, arg4, arg5, arg6):
    filtered_data = athlete_events[(athlete_events[arg1] == arg2) & (athlete_events[arg3] == arg4) & (athlete_events[arg5] == arg6)]
    medal_counts = filtered_data.pivot_table(index='Sport', columns='Medal', values='ID', aggfunc='count', fill_value=0)
    medal_counts.columns = ['Bronze', 'Gold', 'Silver']
    medal_top_10_sports = medal_counts.head(10)
    medal_top_10_sports['Total'] = medal_top_10_sports.sum(axis=1)
    medal_top_10_sports.sort_values(by='Total', inplace=True, ascending=True)
    return medal_top_10_sports

def medal_breakdown_athletes_none_selected():
    medal_breakdown = athlete_events.groupby(['Name', 'Medal'])['Medal'].count().reset_index(name='Count')
    top_10_athletes = medal_breakdown.groupby('Name')['Count'].sum().nlargest(10).index
    top_10_athletes_medal_breakdown = medal_breakdown[medal_breakdown['Name'].isin(top_10_athletes)]
    top_10_athletes_medal_breakdown['Total'] = top_10_athletes_medal_breakdown.groupby('Name')['Count'].transform('sum')
    top_10_athletes_medal_breakdown.sort_values(by='Total', ascending=True, inplace=True)
    return top_10_athletes_medal_breakdown

def medal_breakdown_athletes_single_selected(arg1, arg2):
    athlete_medal_count = athlete_events[athlete_events[arg1] == arg2].groupby(['Name', 'Medal'])['Medal'].count().reset_index(name='Count')
    top_10_athletes = athlete_medal_count.groupby('Name')['Count'].sum().nlargest(10).index
    top_10_athletes_medal_breakdown = athlete_medal_count[athlete_medal_count['Name'].isin(top_10_athletes)]
    top_10_athletes_medal_breakdown['Total'] = top_10_athletes_medal_breakdown.groupby('Name')['Count'].transform('sum')
    top_10_athletes_medal_breakdown.sort_values(by='Total', ascending=True, inplace=True)
    return top_10_athletes_medal_breakdown

def medal_breakdown_athletes_double_selected(arg1, arg2, arg3, arg4):
    athlete_medal_count = athlete_events[(athlete_events[arg1] == arg2) & (athlete_events[arg3] == arg4)].groupby(['Name', 'Medal'])['Medal'].count().reset_index(name='Count')
    top_10_athletes = athlete_medal_count.groupby('Name')['Count'].sum().nlargest(10).index
    top_10_athletes_medal_breakdown = athlete_medal_count[athlete_medal_count['Name'].isin(top_10_athletes)]
    top_10_athletes_medal_breakdown['Total'] = top_10_athletes_medal_breakdown.groupby('Name')['Count'].transform('sum')
    top_10_athletes_medal_breakdown.sort_values(by='Total', ascending=True)
    return top_10_athletes_medal_breakdown

def medal_breakdown_athletes_triple_selected(arg1, arg2, arg3, arg4, arg5, arg6):
    athlete_medal_count = athlete_events[(athlete_events[arg1] == arg2) & (athlete_events[arg3] == arg4) & (athlete_events[arg5] == arg6)].groupby(['Name', 'Medal'])['Medal'].count().reset_index(name='Count')
    athletes_medal_breakdown = athlete_medal_count
    athletes_medal_breakdown['Total'] = athletes_medal_breakdown.groupby('Name')['Count'].transform('sum')
    athletes_medal_breakdown.sort_values(by='Total', ascending=True, inplace=True)
    top_10_athletes_medal_breakdown = athletes_medal_breakdown.tail(10)
    return top_10_athletes_medal_breakdown