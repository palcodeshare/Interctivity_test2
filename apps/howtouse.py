import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly
import plotly.tools as tls

from app import app

layout = html.Div(
    [
        dcc.Location(
             id='url2'
        ),

        html.Div([
            html.Div([
                html.H1(
                    'GfK ONE - POS DASHBOARD',
                    className='five columns',
                )
            ],style={'color': '#FF8C00'}),

            html.Img(
                src="https://www.gfk.com/fileadmin/fe/gfktheme/images/favicons/apple-touch-icon-72x72.png",
                className='one columns',
                style={
                    'height': '70',
                    'width': '70',
                    'float': 'right',
                    'position': 'relative',
                },
            ),
        ],className='row'),
        html.Br(),
        html.Div([
            html.Button('Dashboard', id='button1', style={'width':'180px','color': '#FF8C00','fontWeight': 'bold','font-family': 'Calibri Light','fontSize':'14'}, className='one column'),
            html.Button('Notes', id='button2', style={'width':'180px','color': '#FF8C00','fontWeight': 'bold','font-family': 'Calibri Light','fontSize':'14'}, className='one column'),
        ],className='row'),
        dcc.Markdown('''---'''),
        html.Div([
            html.H2(
                'Navigating The Dashboard',
                className='five columns',
            )
        ],style={'color': '#FF8C00'}),

    ],style={'font-family': 'Calibri Light'},className='ten columns offset-by-one'
)

@app.callback(Output('url2', 'pathname'),
              [Input('button1', 'n_clicks')])

def render_content(clickData):
    if clickData > 0:
        return '/apps/shelldashboard'
