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

print(dcc.__version__)

#app = dash.Dash()
#server = app.server

#Bootstrap CSS
#app.css.append_css({'external_url': 'https://codepen.io/mokshaxkrodha/pen/XBXNbP'})

#app = dash.Dash('auth')
#auth = dash_auth.BasicAuth(
#    app,
#    (('abcd','1234',),)
#)

#Flask hosting
server = flask.Flask('app')
server.secret_key = os.environ.get('secret_key', 'secret')

#Dash app

app = dash.Dash('app',server=server)

app.config.suppress_callback_exceptions = True


index_page = html.Div([
    dcc.Link('Go to Page 1', href='/apps/app1'),
])
