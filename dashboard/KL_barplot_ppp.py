import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
pio.templates.default = "plotly_dark"

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import os



# load your data
df = pd.read_csv('sorted_county_income_ppp.csv')


# Get checklist options
all_counties = df.county.unique()


# idk what this does; prepare your app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

# create your app layout
app.layout = html.Div([
    
    # create your checklist button for county selection
    dcc.Dropdown(
        
        id = "dropdown",
        
        options = [{"label": x, "value": x} 
                 for x in all_counties],
        
        value = all_counties[0],
        multi = False,
        placeholder = "Select a county in California"
        
    ),
    
    # create your button for 
    
    
    dcc.Graph(id = "scatter"),
    
])


# Setup callback function
@app.callback(
    Output("scatter", "figure"), 
    [Input("dropdown", "value")])



# Plot your PPP loan comparison by income group based on user input
def update_line_chart(county):
    
    # create your mask filter
    temp = df.loc[df['county'] == county]
    
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

    # Add figure title
    fig.update_layout(
        title_text = "Loans distributed by income group"
    )

    # Set x-axis title
    fig.update_xaxes(title_text = "Income Group")

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Proportion</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Loan Amount</b>", secondary_y=True)

 
    return fig


# Run your dash app
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port="8050", debug = True)











