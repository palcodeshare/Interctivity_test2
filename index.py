import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_auth
from app import app
from apps import shelldashboard,howtouse,notes
import os

app.config['suppress_callback_exceptions']=True
server = app.server
server.secret_key = os.environ.get('secret_key', 'secret')
auth = dash_auth.BasicAuth(
    app,
    (('Retailaudit','Distributionkpis',),('gfkinternal','gfkoneposdb',),('aajaya','gfkoneposdb37',),)
)

app.layout = html.Div([
            dcc.Location(id='url',refresh=True),
            html.Div(id='page-content')
        ])


# myauthenticateduser = 'gfkinternal'
# print(myauthenticateduser)

@app.callback(Output('page-content', 'children'),
                      [Input('url', 'pathname')])
def display_page(pathname):
    myauthenticateduser = auth._username
    if myauthenticateduser == 'gfkinternal':
        if pathname == '/apps/shelldashboard':
             return shelldashboard.layout
        elif pathname == '/apps/howtouse':
             return howtouse.layout
        elif pathname == '/apps/notes':
             return notes.layout
        else:
            return shelldashboard.layout
    elif myauthenticateduser == 'Retailaudit':
        if pathname == '/apps/shelldashboard':
             return shelldashboard.layout
        elif pathname == '/apps/howtouse':
             return howtouse.layout
        elif pathname == '/apps/notes':
             return notes.layout
        else:
            return shelldashboard.layout
    elif myauthenticateduser == 'aajaya':
        if pathname == '/apps/shelldashboard0':
             return shelldashboard.layout
        elif pathname == '/apps/howtouse':
             return howtouse.layout
        elif pathname == '/apps/notes':
             return notes.layout
        else:
            return shelldashboard0.layout

if __name__ == '__main__':
    app.run_server(debug=True)
