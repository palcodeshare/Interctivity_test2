import numpy as np
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


import  plotly.plotly as py
import plotly.graph_objs as go

from app import app


mapbox_access_token = "pk.eyJ1IjoiamFja3AiLCJhIjoidGpzN0lXVSJ9.7YK6eRwUNFwd3ODZff6JvA"

df = pd.read_csv('lat_lon_counties.csv',encoding='cp1252')
#df_lat_lon['FIPS'] = df_lat_lon['FIPS'].apply(lambda x: str(x).zfill(5))

#app = dash.Dash()


# example measurement stations
lats = [29.2985,21.9162]
lons = [42.5510,95.9560]
text = ['ME','APAC']

# clickme = html.Div([
#     html.Div(id='change_page'),
#     dcc.Location(id='href='/apps/app1')
# ])
fig= go.Figure(
    data=[
        # dict(
        #     type = 'choropleth',
        #     locations=['ARE','AFG','ALB'],
        #     colorscale = [[0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"]],
        #     autocolorscale = False,
        #     reversescale = True,
        #     marker = dict(
        #         line = dict (
        #             color = 'rgb(180,180,180)',
        #             width = 0.5
        #     ) ),
        #     # lat = lats,
        #     # lon = lons,
        #     # mode = "markers",
        #     # marker = dict(size=8,color='rgb(255, 0, 0)',opacity=0.7),
        #     # text = text
        # )

        dict(
            type = "scattermapbox",
            lat = lats,
            lon = lons,
            mode = "markers",
            marker = dict(size=200,color='rgb(242, 177, 172)',opacity=0.3),
            text = text

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
            zoom = 2.5,
            layers = [],
        )
    )
)

layout = html.Div([
    # map centered to USA
    dcc.Location(
         id='url1'
    ),

    html.Div([
        html.H1(
            children='GfK POS DASHBOARD',
            style={'font-weight': 'bold'}
        )
    ],style = {'font-family': 'insight Display screen','text-align' : 'center'}, className = "row"),

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
    ],style={'font-family': 'insight screen'}, className = "row"),


    html.Div([
        html.H3(
            children='Select Region :'
        )
    ],style={'font-family': 'insight display screen','text-align': 'center'},className = "row"),

    html.Div([
        dcc.Graph(
            id = "mapbox",
            figure= go.Figure(
                data=[
                    dict(
                        type = "scattermapbox",
                        lat = lats,
                        lon = lons,
                        mode = "markers",
                        marker = dict(size=200,color='rgb(242, 177, 172)',opacity=0.3),
                        text = text
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
            config={'scrollZoom': False}
        )
    ], style = {"border-style": "solid", "height": "60vh","border-width": "2px",'font-family': 'insight screen'},className = "row"),
])

@app.callback(
    Output('url1','pathname'),
    [Input('mapbox', 'clickData')]
)

def change_page(clickData):
    print(str(clickData['points'][0]['pointNumber']))
    if str(clickData['points'][0]['pointNumber'])==str(1):
        return '/apps/app4'
    elif str(clickData['points'][0]['pointNumber'])==str(0):
        return '/apps/app4'

if __name__ == "__main__":
    app.run_server(debug=True)
