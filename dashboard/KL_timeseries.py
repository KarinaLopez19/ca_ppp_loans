import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import os
import plotly.io as pio
pio.templates.default = "plotly_dark"


# load your data
df = pd.read_csv('state_industry_revenue.csv')


# Get checklist options
all_industries = df.industry_group.unique()


# idk what this does; prepare your app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

# create your app layout
app.layout = html.Div([
    
    # create your checklist button
    dcc.Checklist(
        
        id = "checklist",
        
        options = [{"label": x, "value": x} 
                 for x in all_industries],
        
        value = all_industries[3:],
        labelStyle = {'display': 'inline-block'}
    ),
    
    
    dcc.Graph(id = "line-chart"),
    
])


# Setup callback function
@app.callback(
    Output("line-chart", "figure"), 
    [Input("checklist", "value")])



# Update your line chart based on user input
def update_line_chart(continents):
    
    # create your mask filter
    mask = df.industry_group.isin(continents)
    
    # plot your timeseries line plot
    fig = px.line(df[mask], x = 'date', y = 'revenue_change', color = 'industry_group')
    fig.add_hline(y = 0, line_dash = "dot",
              annotation_text = "Baseline rate of change",
              annotation_position = "bottom right")
    
    # Add pre-covid period
    fig.add_vrect(x0 = "2020-01-10", x1 = "2020-03-13", col = 1,
              annotation_text = "Pre-COVID", annotation_position = "top left",
              fillcolor = "blue", opacity = 0.25, line_width = 0)   
    
    
    # Update your titles
    fig.update_layout(legend_title_text = 'Industry',
        title_text = "<b>Changes in revenue by industry<b>"
    )
    
    # Set x-axis title
    fig.update_xaxes(title_text = "<b>Date<b>", )

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Change in revenue</b>", secondary_y=False)
    
    
    return fig


# Run your dash app
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port="8050", debug = True)








