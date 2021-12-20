"""Instantiate a Dash app."""
import numpy as np
import pandas as pd
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from .data import create_dataframe
from .layout import html_layout
import plotly.express as px
import json 

import string
import random
  
# initializing size of string 
N = 7
from flask import Flask, render_template, redirect, url_for, session, request
import urllib.parse
import flask



def dashboard(server,  messages,dash_app):
    """Create a Plotly Dash dashboard."""    

    
    with server.test_request_context('/dashboard/'):
       df = create_dataframe(json.loads(messages)["dataFrame"], server)

    # Custom HTML layout
    dash_app.index_string = html_layout

    fig = px.scatter_matrix(df)
    # Create Layout
    dash_app.layout = html.Div(
        children=[dcc.Graph(
            id='histogram-graph',
            figure=fig),
            create_data_table(df)
        ],
        id='dash-container'
    )
    return dash_app.server


def create_data_table(df):
    """Create Dash datatable from Pandas DataFrame."""
    table = dash_table.DataTable(
        id='database-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        sort_action="native",
        sort_mode='native',
        page_size=300
    )
    return table