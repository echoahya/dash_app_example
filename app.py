
# coding: utf-8

# Final Project
# Create a Dashboard taking data from Eurostat, GDP and main components (output, expenditure and income). The dashboard will have two graphs:
# - The first one will be a scatterplot with two DropDown boxes for the different indicators. It will have also a slide for the different years in the data.
# - The other graph will be a line chart with two DropDown boxes, one for the country and the other for selecting one of the indicators. (hint use Scatter object using mode = 'lines'

# In[2]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import pandas as pd
import numpy as np


# In[3]:


df = pd.read_csv('Eurostat.csv', index_col=0)
print(df.head())


# In[ ]:





# In[7]:


app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

available_indicators = df['Indicator'].unique()

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in df['Country'].unique()],
                value='Belgium'
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

])

@app.callback(
    dash.dependencies.Output('Eurostat', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name):
    
    return {
        'data': [go.Scatter(
            
            
            x=df[(df['Country'] == xaxis_column_name) & (df['Indicator'] == yaxis_column_name)]['Year'],
            y=df[(df['Country'] == xaxis_column_name) & (df['Indicator'] == yaxis_column_name)]['Value'],
            text=df[df['Indicator'] == yaxis_column_name]['Country'],
            mode='lines',
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

if __name__ == '__main__':
    app.run_server()


# In[ ]:




