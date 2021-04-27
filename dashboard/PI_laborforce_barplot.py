import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy
import geopandas as gpd
import matplotlib
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] #brings in a css file for style guildelines

app = dash.Dash(__name__, external_stylesheets=external_stylesheets) #creates the app

df = pd.read_csv('final_combined_df.csv', sep=',')
merged_df = df.copy()
merged_df.sort_values('county', inplace = True, ascending=[True])

unemployment_df = pd.read_csv('ca_counties_employment_GEOID.csv', sep=',')
unemployment_df.drop(columns=['date','year','GEOID'], inplace=True)
april_unemp_df = unemployment_df[unemployment_df['month'] == 4]

ppp_jobs = merged_df.groupby('county')['jobs_reported'].sum()
ppp_jobs = ppp_jobs.to_frame().reset_index()

total_merged = pd.merge(april_unemp_df, ppp_jobs, how='inner', on='county')
total_merged['jobs_dif'] = total_merged.labor_force - total_merged.jobs_reported - total_merged.unemployment

counties = total_merged.county


app.layout = html.Div(children=[
    
    # create your checklist button for county selection
    dcc.Dropdown(
        
        id = "dropdown",
        
        options = [{"label": x, "value": x} 
                 for x in counties],
        
        value = counties[0],
        multi = False,
        placeholder = "Select a county in California"
        
    ),
    
    # create your button for 
    
    
    dcc.Graph(id = "labor_force"),
    
])

# Setup callback function
@app.callback(
    Output("labor_force", "figure"), 
    [Input("dropdown", "value")])

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
        height=250,
       )
    fig.update_yaxes(tick0=0.25, dtick=0.5)
    
    return fig

    # create your mask filter

# Run your dash app
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port="8050", debug = True)

