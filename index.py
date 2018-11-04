import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_auth
from app import app
from apps import shelldashboard,howtouse
import os

server = app.server
server.secret_key = os.environ.get('secret_key', 'secret')
auth = dash_auth.BasicAuth(
    app,
    (('Retailaudit','Distributionkpis',),('gfkinternal','gfkoneposdb',),)
)

app.layout = html.Div([
    dcc.Location(id='url',refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/shelldashboard':
         return shelldashboard.layout
    elif pathname == '/apps/howtouse':
         return howtouse.layout
    else:
        return shelldashboard.layout

if __name__ == '__main__':
    app.run_server(debug=True)
