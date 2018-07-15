import dash

app = dash.Dash()
server = app.server
app.config.suppress_callback_exceptions = True

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

index_page = html.Div([
    dcc.Link('Go to Page 1', href='/apps/app1'),
])
