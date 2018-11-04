import dash
import os
import config
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly
import plotly.tools as tls
import base64

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
        ],className='row',style={'color': '#FF8C00'}),
        html.Br(),
        html.Div([
            html.P('1. Select a desired region from the horizontal tab on top of the page. By default, the dashboard views the global overview.'),
            html.Img(src='image/tabs.png'),
            html.P('2. For all regions (MESA/RUSSIA/APAC/CHINA/EU) select the analysis type (By Channel/By Region). Data is viewable in terms of channels or regions but not both simultaneously. At any point, any single option can be active.'),
            html.P('3. Select the desired values from the dropdown menus. Choosing dropdown values sequentially from left to right is advised as available options are displayed as per preceeding selections.'),
            html.P('4. Charts can be zoomed in by clicking and dragging the zoom box on the desired location on the chart. Subsequently, you can zoom out to default view by double clicking anywhere on the chart.'),
            html.Br(),
            html.Br(),
            html.P('For any queries please email to nilay.doshi@gfk.com')

        ]),

    ],style={'font-family': 'Calibri Light'},className='ten columns offset-by-one'
)

@app.callback(Output('url2', 'pathname'),
              [Input('button1', 'n_clicks')])

def render_content(clickData):
    if clickData > 0:
        return '/apps/shelldashboard'
