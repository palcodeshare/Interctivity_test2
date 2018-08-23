import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import psycopg2
import os
import flask
import plotly
from plotly.offline import init_notebook_mode, iplot

from app import app
from apps import app4



app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/app4':
         return app4.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)
