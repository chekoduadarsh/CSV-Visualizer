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

from dash.dependencies import Input, Output, State
import string
import random
  
from flask import Flask, render_template, redirect, url_for, session, request
import urllib.parse
import flask



def dashboard(server,  messages,dash_app):
    """Create a Plotly Dash dashboard."""    

    
    with server.test_request_context('/dashboard/'):
       df = create_dataframe(json.loads(messages)["dataFrame"], server)


    dropdowns = []

    for column in df.columns:
        dropdowns.append({"label":column, "value":column})
    barmode = [{"label":"stack", "value":"stack"},{"label":"group", "value":"group"}]
    # Custom HTML layout
    dash_app.index_string = html_layout

    # Create Layout
    dash_app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab-1',  children=[

        dcc.Tab(label='DataFrame View', value='tab-1' , children = [    
            create_data_table(df)
        ]),
        dcc.Tab(label='Scatter Plot', value='tab-2', children = [

            html.Div( id='input-1', children = [  
            dcc.Dropdown(id='input-x-scatter', options=dropdowns, placeholder='Enter X axis Value'),
            dcc.Dropdown(id='input-y-scatter', options=dropdowns, placeholder='Enter Y axis Value'),
            ]),

            html.Div( id='input-2', children = [                    
            dcc.Dropdown(id='input-color-scatter', options=dropdowns, placeholder='Enter Color axis Value'),
            dcc.Dropdown(id='input-size-scatter', options=dropdowns, placeholder='Enter Size axis Value'),
            ]),
           

            html.Button(id='submit-button-scatter', n_clicks=0, children='Submit'),

            html.Div(id='output-state-scatter', children = []),
        ]),

        dcc.Tab(label='Line Plot', value='tab-3', children = [

            html.Div( id='input-1', children = [  
            dcc.Dropdown(id='input-x-line', options=dropdowns, placeholder='Enter X axis Value'),
            dcc.Dropdown(id='input-y-line', options=dropdowns, placeholder='Enter Y axis Value'),
            ]),

            html.Div( id='input-2', children = [                    
            dcc.Dropdown(id='input-color-line', options=dropdowns, placeholder='Enter Color axis Value'),
            ]),
           

            html.Button(id='submit-button-line', n_clicks=0, children='Submit'),

            html.Div(id='output-state-line', children = []),
        ]),

        dcc.Tab(label='Bar Graph', value='tab-4' , children = [    
            
            html.Div( id='input-1', children = [  
            dcc.Dropdown(id='input-x-bar', options=dropdowns, placeholder='Enter X axis Value'),
            dcc.Dropdown(id='input-y-bar', options=dropdowns, placeholder='Enter Y axis Value'),
            ]),
            html.Div( id='input-2', children = [                    
            dcc.Dropdown(id='input-color-bar', options=dropdowns, placeholder='Enter Color axis Value'),
            dcc.Dropdown(id='input-barmode-bar', options=barmode, placeholder='Enter BarMode'),
            ]),

            html.Button(id='submit-button-bar', n_clicks=0, children='Submit'),

            html.Div(id='output-state-bar', children = []),
        ]),

         dcc.Tab(label='Pie Chart', value='tab-5' , children = [    
            
            html.Div( id='input-1', children = [  
            dcc.Dropdown(id='input-x-pie', options=dropdowns, placeholder='Enter X axis Value'),
            ]),
            html.Div( id='input-2', children = [                    
            dcc.Dropdown(id='input-names-pie', options=dropdowns, placeholder='Enter names Value'),
            ]),

            html.Button(id='submit-button-pie', n_clicks=0, children='Submit'),

            html.Div(id='output-state-pie', children = []),
        ]),

        dcc.Tab(label='Tree Map', value='tab-6' , children = [    
            
            html.Div( id='input-1', children = [  
            dcc.Dropdown(id='input-x-tree', options=dropdowns, placeholder='Enter Tree Path', multi=True),
            dcc.Dropdown(id='input-value-tree', options=dropdowns, placeholder='Enter Value'),
            ]),
            html.Div( id='input-2', children = [                    
            dcc.Dropdown(id='input-color-tree', options=dropdowns, placeholder='Enter Color Value'),
            ]),

            html.Button(id='submit-button-tree', n_clicks=0, children='Submit'),

            html.Div(id='output-state-tree', children = []),
        ]),

        dcc.Tab(label='Sunburst Chart', value='tab-7' , children = [    
            
            html.Div( id='input-1', children = [  
            dcc.Dropdown(id='input-x-sun', options=dropdowns, placeholder='Enter Chart Path', multi=True),
            dcc.Dropdown(id='input-value-sun', options=dropdowns, placeholder='Enter Value'),
            ]),
            html.Div( id='input-2', children = [                    
            dcc.Dropdown(id='input-color-sun', options=dropdowns, placeholder='Enter Color Value'),
            ]),

            html.Button(id='submit-button-sun', n_clicks=0, children='Submit'),

            html.Div(id='output-state-sun', children = []),
        ]),

         
        dcc.Tab(label='Box Plot', value='tab-8' , children = [    
            
            html.Div( id='input-1', children = [  
            dcc.Dropdown(id='input-x-box', options=dropdowns, placeholder='Enter X axis Value'),
            dcc.Dropdown(id='input-y-box', options=dropdowns, placeholder='Enter Y axis Value'),
            ]),
            html.Div( id='input-2', children = [                    
            dcc.Dropdown(id='input-color-box', options=dropdowns, placeholder='Enter Color axis Value'),
            ]),

            html.Button(id='submit-button-box', n_clicks=0, children='Submit'),

            html.Div(id='output-state-box', children = []),
        ]),

        dcc.Tab(label='Histogram', value='tab-9' , children = [    
            
            html.Div( id='input-1', children = [  
            dcc.Dropdown(id='input-x-hist', options=dropdowns, placeholder='X axis value'),
            ]),
            html.Div( id='input-2', children = [                    
            dcc.Dropdown(id='input-color-hist', options=dropdowns, placeholder='Enter Color Value'),
            ]),

            html.Button(id='submit-button-hist', n_clicks=0, children='Submit'),

            html.Div(id='output-state-hist', children = []),
        ]),


        dcc.Tab(label='HeatMap', value='tab-10' , children = [    
            
            html.Div( id='input-1', children = [  
            dcc.Dropdown(id='input-x-heat', options=dropdowns, placeholder='X axis value'),
            dcc.Dropdown(id='input-y-heat', options=dropdowns, placeholder='Y axis value'),
            ]),
            html.Div( id='input-2', children = [                    
            dcc.Dropdown(id='input-color-heat', options=dropdowns, placeholder='Enter Color Value'),
            ]),

            html.Button(id='submit-button-heat', n_clicks=0, children='Submit'),

            html.Div(id='output-state-heat', children = []),
        ]),
    ]),
    html.Div(id='tabs-content')
    ])  


    @dash_app.callback(Output('output-state-scatter', 'children'),
              Input('submit-button-scatter', 'n_clicks'),
              State('input-x-scatter', 'value'),
              State('input-y-scatter', 'value'),
              State('input-color-scatter', 'value'),
              State('input-size-scatter', 'value'))
    def update_scatterplot(n_clicks, input1, input2, input3, input4): 
        if str(input1) in df.columns and str(input2) in df.columns:
            if (input4 is None) and (input3 is None):
                fig = px.scatter(df, x=str(input1), y=str(input2))
                return dcc.Graph(
                        id='graph-1-tabs',
                        figure=fig
                    )
            if (input4 is None) and not(input3 is None):
                fig = px.scatter(df, x=str(input1), y=str(input2), color=str(input3))
                return dcc.Graph(
                        id='graph-1-tabs',
                        figure=fig
                    )    

            if not(input4 is None) and (input3 is None):
                fig = px.scatter(df, x=str(input1), y=str(input2), size=str(input4))
                return dcc.Graph(
                        id='graph-1-tabs',
                        figure=fig
                    )
            if not(input4 is None) and not(input3 is None):
                fig = px.scatter(df, x=str(input1), y=str(input2), color=str(input3), size=str(input4))
                return dcc.Graph(
                        id='graph-1-tabs',
                        figure=fig
                    )

        return  "Fill the required fields and click on 'Submit' to generate teh graph you want!!"


    @dash_app.callback(Output('output-state-line', 'children'),
              Input('submit-button-line', 'n_clicks'),
              State('input-x-line', 'value'),
              State('input-y-line', 'value'),
              State('input-color-line', 'value'))
    def update_lineplot(n_clicks, input1, input2, input3): 
        input4 = None
        if str(input1) in df.columns and str(input2) in df.columns:
            if (input4 is None) and (input3 is None):
                fig = px.line(df, x=str(input1), y=str(input2))
                return dcc.Graph(
                        id='graph-1-tabs',
                        figure=fig
                    )
            if (input4 is None) and not(input3 is None):
                fig = px.line(df, x=str(input1), y=str(input2), color=str(input3))
                return dcc.Graph(
                        id='graph-1-tabs',
                        figure=fig
                    )    

            if not(input4 is None) and (input3 is None):
                fig = px.line(df, x=str(input1), y=str(input2), size=str(input4))
                return dcc.Graph(
                        id='graph-1-tabs',
                        figure=fig
                    )
            if not(input4 is None) and not(input3 is None):
                fig = px.line(df, x=str(input1), y=str(input2), color=str(input3), size=str(input4))
                return dcc.Graph(
                        id='graph-1-tabs',
                        figure=fig
                    )

        return  "Fill the required fields and click on 'Submit' to generate teh graph you want!!"



    @dash_app.callback(Output('output-state-bar', 'children'),  
              Input('submit-button-bar', 'n_clicks'),
              State('input-x-bar', 'value'),
              State('input-y-bar', 'value'),
              State('input-color-bar', 'value'),
              State('input-barmode-bar', 'value'))
    def update_barplot(n_clicks, input1, input2, input3, input4): 
        if str(input1) in df.columns and str(input2) in df.columns:
            if (input4 is None) and (input3 is None):
                fig = px.bar(df, x=str(input1), y=str(input2))
                return dcc.Graph(
                        id='graph-1-tabs',
                        figure=fig
                    )
            if (input4 is None) and not(input3 is None):
                fig = px.bar(df, x=str(input1), y=str(input2), color=str(input3))
                return dcc.Graph(
                        id='graph-1-tabs',
                        figure=fig
                    )    

            if not(input4 is None) and (input3 is None):
                fig = px.bar(df, x=str(input1), y=str(input2), barmode=str(input4))
                return dcc.Graph(
                        id='graph-1-tabs',
                        figure=fig
                    )
            if not(input4 is None) and not(input3 is None):
                fig = px.bar(df, x=str(input1), y=str(input2), color=str(input3), barmode=str(input4))
                return dcc.Graph(
                        id='graph-1-tabs',
                        figure=fig
                    )

        return  "Fill the required fields and click on 'Submit' to generate teh graph you want!!"
    
    @dash_app.callback(Output('output-state-pie', 'children'),  
              Input('submit-button-pie', 'n_clicks'),
              State('input-x-pie', 'value'),
              State('input-names-pie', 'value'))
    def update_pieplot(n_clicks, input1, input2): 
        input4 = None
        if str(input1) in df.columns:
            if (input2 is None):
                fig = px.pie(df, values=str(input1))
                return dcc.Graph(
                        id='graph-1-tabs',
                        figure=fig
                    )
            if not (input2 is None):
                fig = px.pie(df, values=str(input1), names=str(input2))
                return dcc.Graph(
                        id='graph-1-tabs',
                        figure=fig
                    )
        return  "Fill the required fields and click on 'Submit' to generate teh graph you want!!"

    @dash_app.callback(Output('output-state-tree', 'children'),  
              Input('submit-button-tree', 'n_clicks'),
              State('input-x-tree', 'value'),
              State('input-color-tree', 'value'),              
              State('input-value-tree', 'value'))
    def update_treeplot(n_clicks, input1, input2, input3): 
        if not input1 is None:
            if set(input1).issubset(df.columns):
                if (input2 is None) and (input3 is None):
                    fig = px.treemap(df, path=input1)
                    return dcc.Graph(
                            id='graph-1-tabs',
                            figure=fig
                        )
                if not (input2 is None) and (input3 is None):
                    fig = px.treemap(df, path=input1, color=str(input2))
                    return dcc.Graph(
                            id='graph-1-tabs',
                            figure=fig
                        )
                if (input2 is None) and not(input3 is None):
                    fig = px.treemap(df, path=input1, values=str(input3))
                    return dcc.Graph(
                            id='graph-1-tabs',
                            figure=fig
                        )
                if not (input2 is None) and not(input3 is None):
                    fig = px.treemap(df, path=input1, color=str(input2), values=str(input3))
                    return dcc.Graph(
                            id='graph-1-tabs',
                            figure=fig
                        )

        return  "Fill the required fields and click on 'Submit' to generate teh graph you want!!"

    
    @dash_app.callback(Output('output-state-sun', 'children'),  
              Input('submit-button-sun', 'n_clicks'),
              State('input-x-sun', 'value'),
              State('input-color-sun', 'value'),              
              State('input-value-sun', 'value'))
    def update_sunplot(n_clicks, input1, input2, input3): 
        if not input1 is None:
            if set(input1).issubset(df.columns):
                print(input1)
                if (input2 is None) and (input3 is None):
                    fig = px.sunburst(df, path=input1)
                    return dcc.Graph(
                            id='graph-1-tabs',
                            figure=fig
                        )
                if not (input2 is None) and (input3 is None):
                    fig = px.sunburst(df, path=input1, color=str(input2))
                    return dcc.Graph(
                            id='graph-1-tabs',
                            figure=fig
                        )
                if (input2 is None) and not(input3 is None):
                    fig = px.sunburst(df, path=input1, values=str(input3))
                    return dcc.Graph(
                            id='graph-1-tabs',
                            figure=fig
                        )
                if not (input2 is None) and not(input3 is None):
                    fig = px.sunburst(df, path=input1, color=str(input2), values=str(input3))
                    return dcc.Graph(
                            id='graph-1-tabs',
                            figure=fig
                        )

        return  "Fill the required fields and click on 'Submit' to generate teh graph you want!!"


    @dash_app.callback(Output('output-state-box', 'children'),  
              Input('submit-button-box', 'n_clicks'),
              State('input-x-box', 'value'),
              State('input-y-box', 'value'),
              State('input-color-box', 'value'))
    def update_barplot(n_clicks, input1, input2, input3): 
        input4 = None
        if str(input1) in df.columns and str(input2) in df.columns:
            if (input4 is None) and (input3 is None):
                fig = px.box(df, x=str(input1), y=str(input2))
                return dcc.Graph(
                        id='graph-1-tabs',
                        figure=fig
                    )
            if (input4 is None) and not(input3 is None):
                fig = px.box(df, x=str(input1), y=str(input2), color=str(input3))
                return dcc.Graph(
                        id='graph-1-tabs',
                        figure=fig
                    )    

        return  "Fill the required fields and click on 'Submit' to generate teh graph you want!!"
    
    @dash_app.callback(Output('output-state-hist', 'children'),  
              Input('submit-button-hist', 'n_clicks'),
              State('input-x-hist', 'value'),
              State('input-color-hist', 'value'))
    def update_histogram(n_clicks, input1, input2): 
        print(input1)
        if not input1 is None:
            if input1 in df.columns:
                if (input2 is None):
                    fig = px.histogram(df, x=str(input1))
                    return dcc.Graph(
                            id='graph-1-tabs',
                            figure=fig
                        )
                if not (input2 is None):
                    fig = px.histogram(df, x=str(input1), color=str(input2))
                    return dcc.Graph(
                            id='graph-1-tabs',
                            figure=fig
                        )

        return  "Fill the required fields and click on 'Submit' to generate teh graph you want!!"

  
    @dash_app.callback(Output('output-state-heat', 'children'),  
              Input('submit-button-heat', 'n_clicks'),
              State('input-x-heat', 'value'),
              State('input-y-heat', 'value'),
              State('input-color-heat', 'value'))
    def update_barplot(n_clicks, input1, input2, input3): 
        input4 = None
        if str(input1) in df.columns and str(input2) in df.columns:
            if (input4 is None) and (input3 is None):
                fig = px.density_heatmap(df, x=str(input1), y=str(input2))
                return dcc.Graph(
                        id='graph-1-tabs',
                        figure=fig
                    )
            if (input4 is None) and not(input3 is None):
                fig = px.density_heatmap(df, x=str(input1), y=str(input2), z=str(input3))
                return dcc.Graph(
                        id='graph-1-tabs',
                        figure=fig
                    )    

        return  "Fill the required fields and click on 'Submit' to generate teh graph you want!!"
   
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