import json
import requests
import os
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

import geopandas as gpd
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] #brings in a css file for style guildelines

app = dash.Dash(__name__, external_stylesheets=external_stylesheets) #creates the app

#Paul's Unemployment Choropleth Datasets & Variables

unemployment_df = pd.read_csv('ca_counties_employment_GEOID.csv', sep=',')
temp_df = unemployment_df[unemployment_df.month==4]
max_value = unemployment_df.unemployment_rate.max()

with open('CA_Counties/CA_Counties_gpd_cmp.json') as f:
    geojson = json.load(f)

fig_choropleth = px.choropleth(temp_df, geojson=geojson, locations='county',       
                           color='unemployment_rate',
                           color_continuous_scale="Reds",
                           range_color=(0, max_value),
                           featureidkey="properties.NAME",
                           projection="mercator",
                        labels={'unemployment_rate':'% Rate'},
                         hover_data=["labor_force", "employment"]
                          )
fig_choropleth.update_geos(fitbounds="locations", visible=True)
fig_choropleth.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

####################

#Paul's Labor Force Bar Chart Datasets & Variables

total_merged = pd.read_csv('paul_laborForce.csv', sep=',')

counties = total_merged.county

####################

#Ayesha's Industry Datasets & Variables

final_merged = pd.read_csv('final_combined_df.csv')
industry_ppp_df = pd.read_csv('ayesha_industry_ppp4.csv', sep=',', index_col=0)

#number of employees per industry in thousands
job_counts=final_merged.groupby(['general_industry_title'])['thousands_of_jobs_2019'].mean()
#total loan amount per industry
loan_industry=final_merged.groupby('general_industry_title')['ppp_loan_amount'].sum()
#counts of each industry in dataset
industry_counts=final_merged['general_industry_title'].value_counts()


fig_industry_ppp = make_subplots(specs=[[{"secondary_y": True}]])
fig_industry_ppp.add_trace(
    go.Scatter(
        x=industry_ppp_df.index.tolist(),
        y=industry_ppp_df['Loan Amount per Industry'].tolist(),
        name='Loan Amount per Industry',
        marker=dict(
        color='rgb(102, 166, 30)'
    )
    ),secondary_y=True
)
fig_industry_ppp.add_trace(go.Bar(
    y=industry_ppp_df['Employees per Industry'].round(3).tolist(),
    x=industry_ppp_df.index.tolist(),
    name='Employees per Industry',
    #orientation='h',
    marker=dict(
        color='rgb(228, 26, 28)'
    )
))
fig_industry_ppp.add_trace(go.Bar(
    y=industry_ppp_df['Industry Proportion in Dataset'].round(3).tolist(),
    x=industry_ppp_df.index.tolist(),
    name='Industry Proportion in PPP Dataset',
    #orientation='h',
    marker=dict(
        color='rgb(55, 126, 184)'
    )
))
fig_industry_ppp.update_xaxes(ticks="outside", tickangle=45, tickfont=dict(
        size=8.5))
fig_industry_ppp.update_yaxes(title_text="Proportion Relative to All Industries")
fig_industry_ppp.update_yaxes(title_text="Total Loan Amount ($)", secondary_y=True)
fig_industry_ppp.update_layout(
    autosize=False,
    width=625,
    height=500,
    margin=dict(
        l=50,
        r=50,
        b=5,
        t=20,
        pad=4
    ),
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=0.92,
        font=dict(
            size=10)
))

####################
# Karina's County Income Graph Variables #
####################

# load your data
income_df = pd.read_csv('sorted_county_income_ppp.csv')


# Get checklist options
all_counties = income_df.county.unique()

###################
#Karina's Timeseries Plot Variables
###################

# load your data
industry_revenue = pd.read_csv('state_industry_revenue.csv')


# Get checklist options
all_industries = industry_revenue.industry_group.unique()



#when starting with layout, must always start with a div (creates a rectangle to create something within)
app.layout = html.Div(children=[
    html.H1(children='Test'),

    html.Div(children='''
        This is a test.
    '''),
    
    html.Div(
    [
        dbc.Row(dbc.Col(html.Div("A single column"))),
        dbc.Row(
            [
                dbc.Col(html.Div("One of three columns")),
                dbc.Col(html.Div("One of three columns")),
                dbc.Col(html.Div("One of three columns")),
            ]
           ),
    ]
    ),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Card title", className="card-title"),
                    html.P(
                        "This is where our introduction, background info will go",
                        className="card-text",
                        ),
                    ], className="card-body"),
                ], className="card border-left-success shadow h-30 py-2"),
            ]),  
        ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Loans Distributed by Income Group", className="card-title"),
                    html.P(
                        "Some background info "
                        "on this",
                        className="card-text",
                        ),
                    dcc.Dropdown(
        
                        id = "dropdown_2",
        
                        options = [{"label": x, "value": x} 
                         for x in all_counties],
        
                        value = all_counties[0],
                        multi = False,
                        placeholder = "Select a county in California"
        
                        ),
    
                    dcc.Graph(id = "scatter"),
                    ], className="card-body"),
                ], className="card border-left-primary shadow h-90 py-2"),
            dbc.Card([
                dbc.CardBody([
                    html.H4("Card title", className="card-title"),
                    html.P(
                        "Some quick example text to build on the card title and "
                        "make up the bulk of the card's content PART2.",
                        className="card-text",
                        ),
#                     dcc.Dropdown(
        
#                         id = "dropdown_1",

#                         options = [{"label": x, "value": x} 
#                                  for x in counties],

#                         value = counties[0],
#                         multi = False,
#                         placeholder = "Select a county in California"
#                     ),
                    dcc.Graph(id = "labor_force"),
                    ], className="card-body"),
                ], className="card border-left-primary shadow h-10 py-2"),
            ]),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("California County Unemployment Data - Jan-Oct 2020", className="card-title"),
                    html.P(
                        "Use the slider below to see how unemployment changed over"
                        " January to October 2020. Click on a county to get more insights.",
                        className="card-text",
                        ),
    
                    dcc.Graph(
                        id='choropleth1',
                        figure=fig_choropleth),
                    dcc.Slider(
                        id='month-slider',
                        min=unemployment_df['month'].min(),
                        max=unemployment_df['month'].max(),
                        value=unemployment_df['month'].max(),
                        marks={str(month): str(month) for month in unemployment_df['month'].unique()},
                        step=None),
                        ], className="card-body"),
                ], className="card border-left-primary shadow h-100 py-2"),
            ])
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Card title", className="card-title"),
                    html.P(
                        "Some quick example text to build on the card title and "
                        "make up the bulk of the card's content PART1.",
                        className="card-text",
                        ),
                    ], className="card-body"),
                ], className="card border-left-success shadow h-30 py-2"),
            ]),  
        ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Card title", className="card-title"),
                    html.P(
                        "Some quick example text to build on the card title and "
                        "make up the bulk of the card's content PART1.",
                        className="card-text",
                        ),
                    dcc.Graph(
                        id='industry_ppp',
                        figure=fig_industry_ppp),
                    ], className="card-body"),
                ], className="card border-left-success shadow h-400 py-2"),
            ]),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Changes in Revenue by Industry", className="card-title"),
                    html.P(
                        "Some quick example text to build on the card title and "
                        "make up the bulk of the card's content PART1.",
                        className="card-text",
                        ),
                    dcc.Checklist(
        
                        id = "checklist",

                        options = [{"label": x, "value": x} 
                                 for x in all_industries],

                        value = all_industries[3:],
                        labelStyle = {'display': 'inline-block'}
                    ),


                    dcc.Graph(id = "line-chart"),
                        ], className="card-body"),
                ], className="card border-left-success shadow h-200 py-2"),
            ])
    ])
])

@app.callback(
    Output("scatter", "figure"), 
    [Input("dropdown_2", "value")])



# Plot your PPP loan comparison by income group based on user input
def update_line_chart(county):
    
    # create your mask filter
    temp = income_df.loc[income_df['county'] == county]
    
    # Create figure with secondary y-axis
    fig = make_subplots(specs = [[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Bar(x = temp['median_household_income_qr'], y = temp['ppp_income_proportion'], name = "Proportion of loans distributed"),
        secondary_y = False,
    )

    fig.add_trace(
        go.Scatter(x = temp['median_household_income_qr'], y = temp['ppp_income_avg'], name = "Average loan amount"),
        secondary_y = True,
    )

    # Set x-axis title
    fig.update_xaxes(title_text = "Income Group")

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Proportion</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Loan Amount</b>", secondary_y=True)
    
    fig.update_layout(
                     autosize=True,
                     height=325,
                     margin=dict(
                        l=25,
                        r=25,
                        b=50,
                        t=15,
            ),
       )
 
    return fig

@app.callback(
    Output("labor_force", "figure"), 
    [Input("dropdown_2", "value")])

# Plot your PPP loan comparison by income group based on user input
def update_bar_chart(county):
    county_choice = total_merged[total_merged.county == county]

    fig = go.Figure(data=[
        go.Bar(name='Additional Employed', y=county_choice.county, x=county_choice.jobs_dif, orientation='h'),
        go.Bar(name='Workers Benefitted', y=county_choice.county, x=county_choice.jobs_reported, orientation='h'),
        go.Bar(name='Unemployed', y=county_choice.county, x=county_choice.unemployment, orientation='h'),
    ])

    fig.update_layout(barmode='stack',
                     autosize=True,
                     height=100,
                     margin=dict(
                        l=25,
                        r=25,
                        b=25,
                        t=15,
            ),
       )
    fig.update_yaxes(tick0=0.25, dtick=0.5, showticklabels=False)
    
    return fig

# Setup callback function
@app.callback(
    Output("line-chart", "figure"), 
    [Input("checklist", "value")])



# Update your line chart based on user input
def update_line_chart(continents):
    
    # create your mask filter
    mask = industry_revenue.industry_group.isin(continents)
    
    # plot your timeseries line plot
    fig = px.line(industry_revenue[mask], x = 'date', y = 'revenue_change', color = 'industry_group')
    fig.add_hline(y = 0, line_dash = "dot",
              annotation_text = "Baseline rate of change",
              annotation_position = "bottom right")
    
    # Add pre-covid period
    fig.add_vrect(x0 = "2020-01-10", x1 = "2020-03-13", col = 1,
              annotation_text = "Pre-COVID", annotation_position = "top left",
              fillcolor = "blue", opacity = 0.25, line_width = 0)   
    
    
    # Update your titles
    fig.update_layout(legend_title_text = 'Industry',
    )
    
    # Set x-axis title
    fig.update_xaxes(title_text = "<b>Date<b>", )

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Change in revenue</b>", secondary_y=False)
    
    return fig

#the below makes your app run 
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port="8050", debug=True)