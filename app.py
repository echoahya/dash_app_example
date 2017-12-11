
# coding: utf-8

# Final Project
# Create a Dashboard taking data from Eurostat, GDP and main components (output, expenditure and income). The dashboard will have two graphs:
# - The first one will be a scatterplot with two DropDown boxes for the different indicators. It will have also a slide for the different years in the data.
# - The other graph will be a line chart with two DropDown boxes, one for the country and the other for selecting one of the indicators. (hint use Scatter object using mode = 'lines'

# In[17]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import pandas as pd
import numpy as np


# In[18]:


df = pd.read_csv('Eurostat.csv', index_col=0)
print(df.head())


# In[19]:


app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

available_indicators = df['Indicator'].unique()

app.layout = html.Div([
        
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            ),
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Value added, gross'
            ),
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='Eurostat'),

    dcc.Slider(
        id='year--slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].max(),
        step=None,
        marks={str(year): str(year) for year in df['Year'].unique()}
    ),  
              
    
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column1',
                options=[{'label': i, 'value': i} for i in df['Country'].unique()],
                value='Belgium'
            ),
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Value added, gross'
            ),
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='Eurostat1')
   
])


@app.callback(
    dash.dependencies.Output('Eurostat', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 year_value):
    dff = df[df['Year'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['Indicator'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator'] == yaxis_column_name]['Value'],
            text=dff[dff['Indicator'] == yaxis_column_name]['Country'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                
            },
            yaxis={
                'title': yaxis_column_name,
                
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }


@app.callback(
    dash.dependencies.Output('Eurostat1', 'figure'),
    [dash.dependencies.Input('xaxis-column1', 'value'),
     dash.dependencies.Input('yaxis-column1', 'value')])
def update_graph(xaxis_column1_name, yaxis_column1_name):
    
    return {
        'data': [go.Scatter(
            
            
            x=df[(df['Country'] == xaxis_column1_name) & (df['Indicator'] == yaxis_column1_name)]['Year'],
            y=df[(df['Country'] == xaxis_column1_name) & (df['Indicator'] == yaxis_column1_name)]['Value'],
            text=df[df['Indicator'] == yaxis_column1_name]['Country'],
            mode='lines',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column1_name,
                
            },
            yaxis={
                'title': yaxis_column1_name,
                
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }



if __name__ == '__main__':
    app.run_server()

