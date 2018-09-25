import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


import  plotly.plotly as py
import plotly.graph_objs as go

from app import app


mapbox_access_token = "pk.eyJ1IjoiamFja3AiLCJhIjoidGpzN0lXVSJ9.7YK6eRwUNFwd3ODZff6JvA"

layout = html.Div([

    dcc.Location(
         id='url1'
    ),

    html.Div([
        html.H1(
            children='GfK POS DASHBOARD',
            style={'font-weight': 'bold'}
        )
    ],style = {'font-family': 'Calibri Light','text-align' : 'center'}, className = "row"),

    html.Br(),
    #Cockpit overview
    html.Div([
        html.Div([
            html.H5(
                children='Sales Value',
                style={'font-weight': 'bold'}
            ),

            html.H6(
                children='-14%',
                style={'color' : 'red'},
            )
        ],className= 'three columns',style={'text-align' : 'center'}),

        html.Div([
            html.H5(
                children='Sales Units',
                style={'font-weight': 'bold'}
            ),

            html.H6(
                children='2%',
                style={'color' : 'green'},
            )
        ],className= 'three columns',style={'text-align' : 'center'}),

        html.Div([
            html.H5(
                children='Average Price',
                style={'font-weight': 'bold'}
            ),

            html.H6(
                children='-7%',
                style={'color' : 'red'},
            )
        ],className= 'three columns',style={'text-align' : 'center'}),

        html.Div([
            html.H5(
                children='Overall Distribution',
                style={'font-weight': 'bold'}
            ),

            html.H6(
                children='5.5%',
                style={'color' : 'green'},
            )
        ],className= 'three columns',style={'text-align' : 'center'}),
    ],style={'font-family': 'Calibri Light'}, className = "row"),


    html.Div([
        html.H3(
            children='Select Region :'
        )
    ],style={'font-family': 'Calibri Light','text-align': 'center'},className = "row"),

    html.Div([
        dcc.Graph(
            id = "mapbox",
            figure= go.Figure(
                data=[
                    dict(
                        type = "scattermapbox",
                        lat = '23.8859',
                        lon = '45.0792',
                        mode = "markers",
                        marker = dict(size=200,color='rgb(242, 177, 172)',opacity=0.3),

                    )
                ],
                layout= dict(
                    autosize = True,
                    hovermode = "closest",
                    margin = dict(l = 0, r = 0, t = 0, b = 0),
                    showlegend = False,
                    mapbox = dict(
                        accesstoken = mapbox_access_token,
                        bearing =0,
                        center = dict(lat = 25.2489, lon = 55.3061),
                        style = "dark",
                        pitch = 0,
                        zoom = 2.5,
                        layers = [],
                    )
                )
            ),
            style = {"height": "100%"},
            config={'scrollZoom': False,'zoomControl': false}
        )
    ], style = {"border-style": "solid", "height": "60vh","border-width": "2px",'font-family': 'Calibri Light'},className = "row"),
])

@app.callback(
    Output('url1','pathname'),
    [Input('mapbox', 'clickData')]
)

def change_page(clickData):
    print(str(clickData['points'][0]['pointNumber']))
    if str(clickData['points'][0]['pointNumber'])==str(1):
        return '/apps/dbspace_mena'

if __name__ == "__main__":
    app.run_server(debug=True)
