import os
import pickle
import copy
import datetime as dt
import psycopg2
import pandas as pd
from flask import Flask
from flask_cors import CORS
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.tools as tls
from io import StringIO
import numpy as np

import  plotly.plotly as py
import plotly.graph_objs as go

from app import app

mapbox_access_token = "pk.eyJ1IjoiamFja3AiLCJhIjoidGpzN0lXVSJ9.7YK6eRwUNFwd3ODZff6JvA"
app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501


if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'  # noqa: E501
    })

# from controls import REGION, CHANNEL, VEH_TYPES, BASE, FACT
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()


# Global chart template

# App layout
layout = html.Div(
    [
        #Title and Gfk Image
        html.Div(
            [
                html.H1(
                    'GfK POS DASHBOARD',
                    className='eleven columns',
                ),
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
            ],
            className='row'
        ),
        html.Br(),
        #Flags overview

        #Period Selector/ Quarterly, YTD vs LY & Monthly vs Previous Month
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='flag_period_button',
                    options=[
                        {'label': 'Quarterly', 'value': 'qtr'},
                        {'label': 'Year To Date', 'value': 'ytd'},
                        {'label': 'Monthly', 'value': 'mom'}
                    ],
                    placeholder="Period Comparison"
                ),
            ],className='two columns'),
        ],className='row'),
        

        html.Div([
            dcc.Graph(
                id='flagsoverview',
                config={'displayModeBar': False}
            )
        ],className='row'),
    ],
    style={'font-family': 'insight screen'},className='ten columns offset-by-one'
)

@app.callback(
    Output('flagsoverview','figure'),
    [Input('flag_period_button','value')]
)

def update_flag(period_comparison_name):
    if (period_comparison_name=='mom'):
        SQL="SELECT ctr_tot, momsvol, momsval, momprice FROM flags"
        cur.execute(SQL,(period_comparison_name,))
        result=cur.fetchall()
        ctr_tot_val, momsvol_val, momsval_val, momprice_val = zip(*result)
        # clrred = 'rgb(225,0,0)'
        # clrgrn = 'rgb(0,222,0)'
        # clrs = [clrred]
        y1=np.array(momsvol_val)
        y2=np.array(momsval_val)
        y3=np.array(momprice_val)

        color1=np.array(['rgba(255, 0, 0, 1)']*y1.shape[0])
        color2=np.array(['rgba(255, 0, 0, 1)']*y2.shape[0])
        color3=np.array(['rgba(255, 0, 0, 1)']*y3.shape[0])

        color1[y1<0]='rgba(255, 0, 0, 1)'
        color1[y1>=0]='rgba(0, 205, 0, 1)'
        color2[y2<0]='rgba(255, 0, 0, 1)'
        color2[y2>=0]='rgba(0, 205, 0, 1)'
        color3[y3<0]='rgba(255, 0, 0, 1)'
        color3[y3>=0]='rgba(0, 205, 0, 1)'

        trace1 = go.Bar(y=ctr_tot_val,x=momsvol_val,name="Sales Volume",orientation='h',text=momsvol_val,textposition = 'inside',hoverinfo='skip',marker=dict(color=color1.tolist()))
        trace2 = go.Bar(y=ctr_tot_val,x=momsval_val,name="Sales Value",orientation='h',text=momsval_val,textposition = 'inside',hoverinfo='skip',marker=dict(color=color2.tolist()))
        trace3 = go.Bar(y=ctr_tot_val,x=momprice_val,name="price",orientation='h',text=momprice_val,textposition = 'inside',hoverinfo='skip',marker=dict(color=color3.tolist()))
        fig = tls.make_subplots(rows=1, cols=3,shared_yaxes=True,vertical_spacing=0.02,horizontal_spacing=0.05,subplot_titles=('Sales Volume', 'Sales Value USD','Price USD'))
        fig['layout']['margin'] = {'l': 150, 'r': 40, 'b': 40, 't': 80}


        fig.append_trace(trace1,1,1)
        fig.append_trace(trace2,1,2)
        fig.append_trace(trace3,1,3)
        fig['layout']['xaxis1'].update(showgrid=False,autorange=True)
        fig['layout']['xaxis2'].update(showgrid=False,autorange=True)
        fig['layout']['xaxis3'].update(showgrid=False,autorange=True)
        fig['layout']['yaxis1'].update(showgrid=False,autorange='reversed')

      # fig.append_trace({'x':df.Time,'y':df.Volume,'type':'bar','name':'Volume'},2,1)
        fig['layout'].update(title='Monthly - Jun"'"17 vs Jun"'"18')
        return fig
    elif (period_comparison_name=='qtr'):
        SQL="SELECT ctr_tot, qtrsvol, qtrsval, qtrprice FROM flags"
        cur.execute(SQL,(period_comparison_name,))
        result=cur.fetchall()
        ctr_tot_val, qtrsvol_val, qtrsval_val, qtrprice_val = zip(*result)

        y1=np.array(qtrsvol_val)
        y2=np.array(qtrsval_val)
        y3=np.array(qtrprice_val)

        color1=np.array(['rgba(255, 0, 0, 1)']*y1.shape[0])
        color2=np.array(['rgba(255, 0, 0, 1)']*y2.shape[0])
        color3=np.array(['rgba(255, 0, 0, 1)']*y3.shape[0])

        color1[y1<0]='rgba(255, 0, 0, 1)'
        color1[y1>=0]='rgba(0, 205, 0, 1)'
        color2[y2<0]='rgba(255, 0, 0, 1)'
        color2[y2>=0]='rgba(0, 205, 0, 1)'
        color3[y3<0]='rgba(255, 0, 0, 1)'
        color3[y3>=0]='rgba(0, 205, 0, 1)'

        trace1 = go.Bar(y=ctr_tot_val,x=qtrsvol_val,name="Sales Volume",orientation='h',text=qtrsvol_val,textposition = 'inside',hoverinfo='skip',marker=dict(color=color1.tolist()))
        trace2 = go.Bar(y=ctr_tot_val,x=qtrsval_val,name="Sales Value",orientation='h',text=qtrsval_val,textposition = 'inside',hoverinfo='skip',marker=dict(color=color2.tolist()))
        trace3 = go.Bar(y=ctr_tot_val,x=qtrprice_val,name="price",orientation='h',text=qtrprice_val,textposition = 'inside',hoverinfo='skip',marker=dict(color=color3.tolist()))
        fig = tls.make_subplots(rows=1, cols=3, shared_yaxes=True,vertical_spacing=0.02,horizontal_spacing=0.05,subplot_titles=('Sales Volume', 'Sales Value USD','Price USD'))
        fig['layout']['margin'] = {'l': 150, 'r': 40, 'b': 40, 't': 80}

        fig.append_trace(trace1,1,1)
        fig.append_trace(trace2,1,2)
        fig.append_trace(trace3,1,3)
        fig['layout']['xaxis1'].update(showgrid=False)
        fig['layout']['xaxis2'].update(showgrid=False)
        fig['layout']['xaxis3'].update(showgrid=False)
        fig['layout']['yaxis1'].update(showgrid=False,autorange='reversed')
      # fig.append_trace({'x':df.Time,'y':df.Volume,'type':'bar','name':'Volume'},2,1)
        fig['layout'].update(title='Quarterly - Q2"'"17 vs Q2"'"18')
        return fig
    elif (period_comparison_name=='ytd'):
        SQL="SELECT ctr_tot, ytdsvol, ytdsval, ytdprice FROM flags"
        cur.execute(SQL,(period_comparison_name,))
        result=cur.fetchall()
        ctr_tot_val, ytdsvol_val, ytdsval_val, ytdprice_val = zip(*result)

        y1=np.array(ytdsvol_val)
        y2=np.array(ytdsval_val)
        y3=np.array(ytdprice_val)

        color1=np.array(['rgba(255, 0, 0, 1)']*y1.shape[0])
        color2=np.array(['rgba(255, 0, 0, 1)']*y2.shape[0])
        color3=np.array(['rgba(255, 0, 0, 1)']*y3.shape[0])

        color1[y1<0]='rgba(255, 0, 0, 1)'
        color1[y1>=0]='rgba(0, 205, 0, 1)'
        color2[y2<0]='rgba(255, 0, 0, 1)'
        color2[y2>=0]='rgba(0, 205, 0, 1)'
        color3[y3<0]='rgba(255, 0, 0, 1)'
        color3[y3>=0]='rgba(0, 205, 0, 1)'

        trace1 = go.Bar(y=ctr_tot_val,x=ytdsvol_val,name="Sales Volume",orientation='h',text=ytdsvol_val,textposition = 'inside',hoverinfo='skip',marker=dict(color=color1.tolist()))
        trace2 = go.Bar(y=ctr_tot_val,x=ytdsval_val,name="Sales Value",orientation='h',text=ytdsval_val,textposition = 'inside',hoverinfo='skip',marker=dict(color=color2.tolist()))
        trace3 = go.Bar(y=ctr_tot_val,x=ytdprice_val,name="price",orientation='h',text=ytdprice_val,textposition = 'inside',hoverinfo='skip',marker=dict(color=color3.tolist()))
        fig = tls.make_subplots(rows=1, cols=3, shared_yaxes=True,vertical_spacing=0.02,horizontal_spacing=0.05,subplot_titles=('Sales Volume', 'Sales Value USD','Price USD'))
        fig['layout']['margin'] = {'l': 150, 'r': 150, 'b': 40, 't': 80}


        fig.append_trace(trace1,1,1)
        fig.append_trace(trace2,1,2)
        fig.append_trace(trace3,1,3)

        fig['layout']['xaxis1'].update(showgrid=False,autorange=True)
        fig['layout']['xaxis2'].update(showgrid=False,autorange=True)
        fig['layout']['xaxis3'].update(showgrid=False,autorange=True)
        fig['layout']['yaxis1'].update(showgrid=False,autorange='reversed')
      # fig.append_trace({'x':df.Time,'y':df.Volume,'type':'bar','name':'Volume'},2,1)
        fig['layout'].update(title='Year to Date - YTD"'"17 vs YTD"'"18')
        return fig




app.scripts.config.serve_locally = True
