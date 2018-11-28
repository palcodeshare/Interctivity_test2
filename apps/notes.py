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
             id='url3'
        ),

        dcc.Location(
             id='url4'
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
            html.Button('How To Use', id='button2', style={'width':'180px','color': '#FF8C00','fontWeight': 'bold','font-family': 'Calibri Light','fontSize':'14'}, className='one column'),
        ],className='row'),
        dcc.Markdown('''---'''),
        html.Div([
            html.H2(
                'Regions & Countries Coverage',
                className='five columns',
            )
        ],className='row',style={'color': '#FF8C00'}),
        html.Br(),
        html.Div([
            html.P('The dashboard currently operates on 13 countries segmenteted into 5 regions as below:'),
            html.P('1. MESA (Middle East And South Africa) - United Arab Emirates, Saudi Arabia, Oman, Egypt '),
            html.P('2. RUSSIA '),
            html.P('3. APAC (Asia Pacific) - Indonesia, Malaysia, Thailand '),
            html.P('4. China '),
            html.P('5. EU (Europe) - Italy, Spain, Great Britain, Germany '),
            dcc.Markdown('''---'''),

        ]),
        html.Div([
            html.H2(
                'Important Notes',
                className='five columns',
            )
        ],className='row',style={'color': '#FF8C00'}),
        html.Br(),
        html.Div([
            html.P('Please find critical information on certain data features available in the dashboard below:'),
            html.P('1. SKU information excludes all tradebrands and exclusives from rankings to maintain retailer confidentiality.'),
            html.P('2. EU doesnt have the region functionality as shell is not being reported by regions in the EU countries.'),
            dcc.Markdown('''---'''),
        ]),
        html.Div([
            html.H2(
                'Updates',
                className='five columns',
            )
        ],className='row',style={'color': '#FF8C00'}),
        html.Br(),
        html.Div([
            html.P('[UPDATE] 11/28/2018, 9:03 GMT'),
            html.P('1. Q3 data loaded with Q2 as reference'),
            html.P('2. Spain removed as country. End of reporting period.'),
            html.P('3. Minor bugs fixed to improve loading speed.'),
            dcc.Markdown('''---'''),
            html.Br(),
            html.Br(),
            html.P('For any queries please email to nilay.doshi@gfk.com',style={'color': '#FF8C00'})

        ]),

    ],style={'font-family': 'Calibri Light'},className='ten columns offset-by-one'
)

@app.callback(Output('url3', 'pathname'),
              [Input('button1', 'n_clicks')])

def render_content3(clickData):
    if clickData > 0:
        return '/apps/shelldashboard'

@app.callback(Output('url4', 'pathname'),
              [Input('button2', 'n_clicks')])

def render_content4(clickData):
    if clickData > 0:
        return '/apps/howtouse'
