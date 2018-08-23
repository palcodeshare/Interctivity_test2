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

#Bootstrap CSS
#app.css.append_css({'external_url': 'https://codepen.io/mokshaxkrodha/pen/XBXNbP'})

#app = dash.Dash('auth')
#auth = dash_auth.BasicAuth(
#    app,
#    (('abcd','1234',),)
#)

#Globabl Declarations
#Mapbox initiations
lats = [25.0657005,24.4666691,25.3373699,25.7895298]
lons = [55.1712799,54.3666687,55.4120598,55.9431992]
text = ['Dubai','Abu Dhabi','Sharjah','Northern Emirates']
mapbox_access_token = "pk.eyJ1IjoiamFja3AiLCJhIjoidGpzN0lXVSJ9.7YK6eRwUNFwd3ODZff6JvA"


#Database connection
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

cur.execute("SELECT DISTINCT(region) FROM react_table")
region1=cur.fetchall()
reg_val = [sales[0] for sales in region1]

#Dash app

#app = dash.Dash('app',server=server)

app.css.append_css({'external_url': 'https://codepen.io/mokshaxkrodha/pen/XBXNbP'})

fig= go.Figure(
    data=[
        #N. Emirates
        dict(
            type = "scattermapbox",
            lat = [25.420998413021056],
            lon = [56.080834963437474],
            mode = "markers",
            #line = dict(color = 'rgb(237, 28, 36)'),
            marker = dict(size=12,color='rgb(255, 213, 0)',opacity=1),
            text = ['Northern Emirates']
        ),

        dict(
            type = "scattermapbox",
            lat = [25.420998413021056],
            lon = [56.080834963437474],
            mode = "markers",
            marker = dict(size=110,color='rgb(237, 28, 36)',opacity=0.1),
            text = ['Northern Emirates']

        ),

        #Sharjah
        dict(
            type = "scattermapbox",
            lat = [25.309943565580184],
            lon = [55.645751955624974],
            mode = "markers",
            #line = dict(color = 'rgb(237, 28, 36)'),
            marker = dict(size=12,color='rgb(255, 213, 0)',opacity=1),
            text = ['Sharjah']
        ),

        dict(
            type = "scattermapbox",
            lat = [25.309943565580184],
            lon = [55.645751955624974],
            mode = "markers",
            marker = dict(size=75,color='rgb(237, 28, 36)',opacity=0.1),
            text = ['Sharjah']

        ),

        #Dubai
        dict(
            type = "scattermapbox",
            lat = [25.042745835000268],
            lon = [55.343627932187474],
            mode = "markers",
            #line = dict(color = 'rgb(237, 28, 36)'),
            marker = dict(size=12,color='rgb(255, 213, 0)',opacity=1),
            text = ['Dubai']
        ),

        dict(
            type = "scattermapbox",
            lat = [25.042745835000268],
            lon = [55.343627932187474],
            mode = "markers",
            marker = dict(size=75,color='rgb(237, 28, 36)',opacity=0.1),
            text = ['Dubai']

        ),

        #AUH+AlAin
        dict(
            type = "scattermapbox",
            lat = [24.29397572281303],
            lon = [54.997558596249974],
            mode = "markers",
            marker = dict(size=12,color='rgb(255, 213, 0)',opacity=1),
            text = ['Abu Dhabi']
        ),

        dict(
            type = "scattermapbox",
            lat = [24.29397572281303],
            lon = [54.997558596249974],
            mode = "markers",
            marker = dict(size=200,color='rgb(237, 28, 36)',opacity=0.1),
            text = ['Abu Dhabi']

        )

    ],
    layout= dict(
        autosize = True,
        hovermode = "closest",
        margin = dict(l = 0, r = 0, t = 0, b = 0),
        showlegend = False,
        xaxis=dict(
            fixedrange=True
        ),
        yaxis=dict(
            autorange='reversed',
            fixedrange=True
        ),
        mapbox = dict(
            accesstoken = mapbox_access_token,
            bearing =0,
            center = dict(lat = 25.2489, lon = 55.3061),
            style = "dark",
            pitch = 0,
            zoom = 6.5,
            layers = []
        )
    )
)

layout = html.Div([
    #Title
    html.Div([

        html.H1(
            children='GfK DASHBOARD APPLICATION',
            className = 'six columns',
            style={'font-weight': 'bold','position': 'top','top':'200px','display':'table-cell'}
        ),

        html.Img(
            src="https://www.gfk.com/fileadmin/fe/gfktheme/images/favicons/apple-touch-icon-72x72.png",
            className = 'one columns',
            style={
                'height': '70',
                'width': '70',
                'float': 'right',
                'position': 'relative',
            }
        ),

        html.Img(
            src="https://image.ibb.co/iZDuHT/Webp_net_resizeimage_1.png",
            className = 'one columns',
            style={
                'height': '70',
                'width': '80',
                'float': 'right',
            #   'position': 'relative',
            }
        )
    ],style={'font-family': 'insight display screen', 'verticalAlign': 'middle'}, className = "row"),

    html.Br(),
    #Cockpit overview
    #Headings
    html.Div([
        html.Div([
            html.H5(
                children='Sales Value',
                style={'font-weight': 'bold'}
                ),
        ],className= 'one columns',style={'text-align' : 'center'}),

        html.Div([
            html.H5(
                children='-41%',
                style={'color' : 'green'}
                ),
            html.H6(
                children='Market',
                ),
        ],className= 'one columns',style={'text-align' : 'center'}),

        html.Div([
            html.H5(
                children='-41%',
                style={'color' : 'green'}
                ),
            html.H6(
                children='Shell',
                ),
        ],className= 'one columns',style={'text-align' : 'center'}),

        html.Div([
            html.H5(
                children='Sales Units',
                style={'font-weight': 'bold'}
                ),
        ],className= 'one columns',style={'text-align' : 'center'}),

        html.Div([
            html.H6(
                children='-41%',
                style={'color' : 'green'}
                ),
            html.H6(
                children='Market',
                ),
        ],className= 'one columns',style={'text-align' : 'center'}),

        html.Div([
            html.H6(
                children='-41%',
                style={'color' : 'green'}
                ),
            html.H6(
                children='Shell',
                ),
        ],className= 'one columns',style={'text-align' : 'center'}),

        html.Div([
            html.H5(
                children='Average Price',
                style={'font-weight': 'bold'}
                ),
        ],className= 'one columns',style={'text-align' : 'center'}),

        html.Div([
            html.H6(
                children='-41%',
                style={'color' : 'green'}
                ),
            html.H6(
                children='Market',
                ),
        ],className= 'one columns',style={'text-align' : 'center'}),

        html.Div([
            html.H6(
                children='-41%',
                style={'color' : 'green'}
                ),
            html.H6(
                children='Shell',
                ),
        ],className= 'one columns',style={'text-align' : 'center'}),

        html.Div([
            html.H5(
                children='Distribution',
                style={'font-weight': 'bold'}
                ),
        ],className= 'one columns',style={'text-align' : 'center'}),

        html.Div([
            html.H6(
                children='-41%',
                style={'color' : 'green'}
                ),
            html.H6(
                children='Market',
                ),
        ],className= 'one columns',style={'text-align' : 'center'}),

        html.Div([
            html.H6(
                children='-41%',
                style={'color' : 'green'}
                ),
            html.H6(
                children='Shell',
                ),
        ],className= 'one columns',style={'text-align' : 'center'})

    ],style={'font-family': 'insight screen'}, className="row gs-text-header"),

    # #Sub-Headings
    # html.Div([
    #     #Sales Value
    #     html.Div([
    #         html.H6(
    #             children='Market  |  Shell',
    #             style={'font-weight': 'bold'}
    #             ),
    #         html.H6(
    #             children='14%',
    #             style={'color' : 'green'},
    #             )
    #     ],className= 'three columns',style={'text-align' : 'center'}),
    #
    #     html.Div([
    #         html.H6(
    #             children='Shell',
    #             style={'font-weight': 'bold'}
    #             ),
    #
    #         html.H6(
    #             children='14%',
    #             style={'color' : 'green'},
    #             )
    #     ],className= 'three columns',style={'text-align' : 'center'}),
    #
    #     html.Div([
    #         html.H6(
    #             children='Market',
    #             style={'font-weight': 'bold'}
    #             ),
    #
    #         html.H6(
    #             children='Shell',
    #             style={'font-weight': 'bold'}
    #             ),
    #     ],className= 'three columns',style={'text-align' : 'center'}),
    #
    #     html.Div([
    #         html.H6(
    #             children='Shell',
    #             style={'font-weight': 'bold'}
    #             ),
    #
    #         html.H6(
    #             children='Shell',
    #             style={'font-weight': 'bold'}
    #             ),
    #     ],className= 'three columns',style={'text-align' : 'center'}),
    #
    #     html.Div([
    #         html.H6(
    #             children='Market',
    #             style={'font-weight': 'bold'}
    #             ),
    #
    #         html.H6(
    #             children='Shell',
    #             style={'font-weight': 'bold'}
    #             ),
    #     ],className= 'three columns',style={'text-align' : 'center'}),
    #
    #     html.Div([
    #         html.H6(
    #             children='Market',
    #             style={'font-weight': 'bold'}
    #             ),
    #
    #         html.H6(
    #             children='Shell',
    #             style={'font-weight': 'bold'}
    #             ),
    #     ],className= 'three columns',style={'text-align' : 'center'}),
    # ],style={'font-family': 'insight screen'}, className = "row"),

    html.Br(),
    html.Div([
        dcc.Link(
            html.Button(children='Change Region',style={'font-family': 'insight screen','text-align':'center','height':'36px'},className = "two columns"),
            href='/apps/app3'
        ),

        html.Div([
            dcc.Dropdown(
                id='reg_col',
                options=[{'label': i, 'value': i} for i in reg_val],
                value='Dubai'
            )
        ],style={'text-align':'center'},className = "two columns")
    ],style={'font-family': 'insight screen'},className="row"),

    html.Br(),
    #Graphs
    html.Div([
        dcc.Location(
             id='url2'
        ),
        #Horizontal bar - flags
        html.Div([
            dcc.Graph(
                id = "mapbox",
                figure=fig,
                style = {"height": "100%"},
                config={'scrollZoom': False,'displayModeBar': False}
            )
        ], style = {"border-style": "solid","border-width": "2px" },className = "six columns"),

        html.Div([
            dcc.Graph(id='react-graph'),

            # dcc.Dropdown(
            #     id='reg_col',
            #     options=[{'label': i, 'value': i} for i in reg_val],
            #     value='Dubai'
            # )
        ],className = "six columns"),


    ], style={'font-family': 'insight screen'},className = "row"),

    html.Div([

        html.Div([
            dcc.Graph(id='react-graph2'),

            # dcc.Dropdown(
            #     id='reg_col',
            #     options=[{'label': i, 'value': i} for i in reg_val],
            #     value='Dubai'
            # )
        ]),


    ], style={'font-family': 'insight screen'},className = "row"),

    dcc.Link('Go to App 2', href='/apps/app2'),
    dcc.Link('Go to App 3', href='/apps/app3')
])

@app.callback(
    Output('reg_col','value'),
    [Input('mapbox', 'clickData')]
)

def change_page(clickData):
    print(str(clickData['points'][0]))
    if clickData:
        return str(clickData['points'][0]['text'])

@app.callback(
    Output('react-graph','figure'),
    [Input('reg_col','value')]
)

def update_graph(value):

    SQL="SELECT fruits, sales FROM react_table WHERE region = (%s)"
    cur.execute(SQL,(value,))
    result=cur.fetchall()
    fruits_val, sales_val = zip(*result)
    print(fruits_val)
    # clrred = 'rgb(225,0,0)'
    # clrgrn = 'rgb(0,222,0)'
    # clrs = [clrred]

    return {
        'data': [go.Bar(
            y=fruits_val,
            x=sales_val,
            orientation = 'h'
        )],
    }



app.scripts.config.serve_locally = True
external_css = ["https://codepen.io/mokshaxkrodha/pen/rrmPNP.css",
                "https://codepen.io/chriddyp/pen/bWLwgP.css"]

for css in external_css:
    app.css.append_css({"external_url": css})
