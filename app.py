# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dependencies
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd
import plotly
import numpy as np

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

import csv
from urllib.request import urlopen
import urllib.request


bgcolors = {
    'background': '#13263a',
    'text': '#FFFFFF'
}

#------------------------------
# external JavaScript files
external_scripts = [
    'https://www.google-analytics.com/analytics.js',
    {'src': 'https://cdn.polyfill.io/v2/polyfill.min.js'},
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.10/lodash.core.js',
        'integrity': 'sha256-Qqd/EfdABZUcAxjOkMi8eGEivtdTkh3b65xCZL4qAQA=',
        'crossorigin': 'anonymous'
    }
]

# external CSS stylesheets
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

#-------------------------------------------------------------------------------
#app stuff
app = dash.Dash(__name__,
                external_scripts=external_scripts,
                external_stylesheets=external_stylesheets)


#-------------------------------------------------------------
#run app layout things
# import required figures
from figures import df, cases, fig0, fig1, fig2, fig3, fig8, fig17, fig33
available_selectors = list(cases.columns)[1:]

app.layout = html.Div(children=[
        html.H1(children='A Deeper Look into the Analytics of Covid-19')
        ,html.Div([
            dcc.Dropdown(
                id='figure1-yaxis-column',
                options=[{'label': i, 'value': i} for i in available_selectors],
                value='totalTestResultsIncrease')
        ])
        ,html.Br(),

        html.Div(children='''
        The purpose of this page is to provide a more in-depth analysis of \
        the Covid-19 outbreak. The charts on this page offer a range of \
        analytical views. From daily percent changes and trends for each \
        day of the week, to the slope and moving averages for each outcome.\
        ''')

        ,html.Br(),

        html.Div(children='''
        The data used for this analysis comes from Our World in Data \
        "https://covidtracking.com/api/v1/us/daily.csv". A more detailed \
        description of the data can be found here:
        https://ourworldindata.org/coronavirus-data
        ''')

        ,html.Br(),

        html.Div(children='''
        The charts below provide analysis for the United States.
        ''')

        ,html.Br(),
        
    html.Div(dcc.DatePickerRange(
        id='figure1-xaxis--datepicker',
        min_date_allowed=min(df['date_new']),
        max_date_allowed=max(df['date_new']),
        initial_visible_month=max(df['date_new']),
        end_date=max(df['date_new'])
    ), style={'width': '49%', 'padding': '0px 20px 20px 20px'}),

    html.Div([
        html.Div([
        html.H2("Figure 1"),
        dcc.Graph(id='figure1-bar')
        ], className="six columns"
        ,style={'padding-left': '5%', 'padding-right': '5%'})

        ,html.Br(),

        html.Div([
        html.H2("Figure 2"),
        dcc.Graph(figure=fig1)
        # ])
        ], className="six columns"
        ,style={'padding-left': '5%', 'padding-right': '5%'})

    ], className="row")

        ,html.Br(),

        html.H1(children='Breakdown of Figure 3')

        ,html.Br(),

        html.Div([
        dcc.Graph(figure=fig2)
        ])

        ,html.Br(),

        html.Div([
        dcc.Graph(figure=fig3)
        ])

        ,html.Br(),

        html.H1(children='Distribution Trends of Daily Outcomes')

        ,html.Br(),

        html.Div([
        dcc.Graph(figure=fig8)
        ])

        ,html.Br(),

        html.H1(children='Day of Week Meets Daily Outcomes')

        ,html.Br(),

        html.Div([
        dcc.Graph(figure=fig17)
        ])
        ,html.Br(),

        html.H1(children='5 Day Moving Average Meets % of Daily Outcomes (Rounded)')

        ,html.Br(),

        html.Div([
        dcc.Graph(figure=fig33)
        ])
])

@app.callback(
    Output('figure1-bar', 'figure'),
    [Input('figure1-yaxis-column','value'),
    Input('figure1-xaxis--datepicker',  component_property = 'start_date'),
    Input('figure1-xaxis--datepicker',  component_property = 'end_date')
    ])
def update_graph(yaxis_column_name, start_date, end_date):
  dff = df[(df['date_new'] > start_date) & (df['date_new'] < end_date)]
  fig = px.bar(dff
             ,x="date_new"
             ,y=yaxis_column_name
             ,hover_data=['totalTestResults']
             ,title="<b>Total Covid Tests (Cummulative)</b>")
  
  fig.update_layout(
    template='plotly_dark'
)
  return fig


if __name__ == '__main__':
    app.run_server(debug=True, port='4000')