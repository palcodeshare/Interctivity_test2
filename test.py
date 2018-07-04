import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, State, Output

app = dash.Dash()
app.layout = html.Div([
    html.Div(id='target'),
    dcc.Input(id='input', type='text', value=''),
    html.Button(id='submit', n_clicks=0, children='Save')
])

@app.callback(Output('target', 'children'), [Input('submit', 'n_clicks')],
              [State('input', 'value')])
def callback(n_clicks, state):
    return "callback received value: {}".format(state)


if __name__ == '__main__':
    app.run_server(debug=True)
