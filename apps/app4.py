import os
import pickle
import copy
import psycopg2
from flask import Flask
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
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

# Postgres to python connect through psycopg2
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

        #Period Selector/ Quarterly, YTD vs LY  vs Previous Month
        html.Div([
            html.Div([
                html.Div([
                    html.P('Select period for overall country-wise flags :', style={'display': 'inline-block'}),

                    dcc.Dropdown(
                        id='flag_period_button',
                        options=[
                            {'label': 'Quarterly Growth%', 'value': 'qtr'},
                            {'label': 'Year to Date Growth%', 'value': 'ytd'}
                        ],
                        value='qtr',
                        placeholder="Period Comparison",

                    )
                ],className='four columns',style={'padding-top':'200px','verticalAlign': 'middle'}),

                dcc.Graph(
                    id='flagsoverview',
                    config={'displayModeBar': False},
                    className='eight columns'
                ),
            ],className='row'),

        ]),

        #bubble test
        html.Div([
            html.Div([
                    html.Div([
                        html.P('Select country :', style={'display': 'inline-block'}),
                        dcc.Dropdown(
                            id='country',
                            options=[
                                {'label': 'AE', 'value': 'United Arab Emirates'},
                                {'label': 'KSA', 'value': 'Saudi Arabia'}
                            ],
                            value='United Arab Emirates',
                            placeholder="Country",

                        ),
                        html.Br(),
                        html.P('Select Type of Vehicle :', style={'display': 'inline-block'}),
                        dcc.Dropdown(
                            id='typeveh',
                            placeholder="Type Of Vehicle",
                        ),
                        html.Br(),
                        html.P('Select Channel :', style={'display': 'inline-block'}),
                        dcc.Dropdown(
                            id='channel',
                            placeholder="Channel",
                        )
                    ],className='two columns',style={'padding-top':'100px','verticalAlign': 'middle'}),

                    dcc.Graph(
                        id='bubble_chart',
                        config={'displayModeBar': False},
                        className='ten columns'
                    ),
            ],className='row')

        ])
    ],
    style={'font-family': 'Calibri Light'},className='ten columns offset-by-one'
)

########<Options for dropdowns Callbacks>########

#Vehicle type button options
@app.callback(
    Output('typeveh','options'),
    [Input('country','value')]
)

def update_typeveh(selected_country):

    SQL="SELECT DISTINCT(typeveh) FROM bubble WHERE country=(%s)"
    cur.execute(SQL,(selected_country,))
    result=cur.fetchall()
    typeveh_options = zip(*result)
    print(typeveh_options)
    opt=np.array(list(typeveh_options))
    print(opt)
    return [{'label': i, 'value': i} for i in opt[0]]

@app.callback(Output('typeveh', 'value'),
              [Input('typeveh', 'options')]
)

def set_typeveh_value(available_options):
    return available_options[1]['value']

#Channel button options
@app.callback(
    Output('channel','options'),
    [Input('country','value'),
     Input('typeveh','value')]
)

def update_typeveh(selected_country,
                   selected_typeveh):

    SQL="SELECT DISTINCT(channel) FROM bubble WHERE country=(%s) AND typeveh=(%s)"
    cur.execute(SQL,(selected_country,selected_typeveh,))
    result=cur.fetchall()
    channel_options = zip(*result)
    print(channel_options)
    opt=np.array(list(channel_options))
    print(opt)
    return [{'label': i, 'value': i} for i in opt[0]]

@app.callback(Output('channel', 'value'),
              [Input('channel', 'options')]
)

def set_typeveh_value(available_options):
    return available_options[2]['value']

########<Flag Chart Callbacks>########
@app.callback(
    Output('flagsoverview','figure'),
    [Input('flag_period_button','value')]
)

def update_flag(period_comparison_name):

    if (period_comparison_name=='qtr'):
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

        trace1 = go.Bar(y=ctr_tot_val,x=qtrsvol_val,name="Sales Volume",orientation='h',text=qtrsvol_val,textposition = 'auto',hoverinfo='skip',marker=dict(color=color1.tolist()),showlegend=False)
        trace2 = go.Bar(y=ctr_tot_val,x=qtrsval_val,name="Sales Value",orientation='h',text=qtrsval_val,textposition = 'auto',hoverinfo='skip',marker=dict(color=color2.tolist()),showlegend=False)
        trace3 = go.Bar(y=ctr_tot_val,x=qtrprice_val,name="price",orientation='h',text=qtrprice_val,textposition = 'auto',hoverinfo='skip',marker=dict(color=color3.tolist()),showlegend=False)
        fig = tls.make_subplots(rows=1, cols=3, shared_yaxes=True,vertical_spacing=0.02,horizontal_spacing=0.05,subplot_titles=('Sales Volume', 'Sales Value USD','Price USD'))
        fig['layout']['margin'] = {'l': 150, 'r': 40, 'b': 40, 't': 100}
        fig['layout'].update(title='Quarterly Growth%',titlefont=dict(family='Calibri Light'))

        fig.append_trace(trace1,1,1)
        fig.append_trace(trace2,1,2)
        fig.append_trace(trace3,1,3)

        for i in fig['layout']['annotations']:
            i['font'] = dict(family='Calibri Light',size=15)

        fig['layout']['xaxis1'].update(showgrid=False,range=[-100,100],showticklabels=False)
        fig['layout']['xaxis2'].update(showgrid=False,range=[-100,100],showticklabels=False)
        fig['layout']['xaxis3'].update(showgrid=False,range=[-100,100],showticklabels=False)
        fig['layout']['yaxis1'].update(showgrid=False,autorange='reversed')
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

        trace1 = go.Bar(y=ctr_tot_val,x=ytdsvol_val,name="Sales Volume",orientation='h',text=ytdsvol_val,textposition = 'auto',hoverinfo='skip',marker=dict(color=color1.tolist()),showlegend=False)
        trace2 = go.Bar(y=ctr_tot_val,x=ytdsval_val,name="Sales Value",orientation='h',text=ytdsval_val,textposition = 'auto',hoverinfo='skip',marker=dict(color=color2.tolist()),showlegend=False)
        trace3 = go.Bar(y=ctr_tot_val,x=ytdprice_val,name="price",orientation='h',text=ytdprice_val,textposition = 'auto',hoverinfo='skip',marker=dict(color=color3.tolist()),showlegend=False)
        fig = tls.make_subplots(rows=1, cols=3, shared_yaxes=True,vertical_spacing=0.02,horizontal_spacing=0.05,subplot_titles=('Sales Volume', 'Sales Value USD','Price USD'))
        fig['layout']['margin'] = {'l': 150, 'r': 20, 'b': 40, 't': 100}
        fig['layout'].update(title='Year to Date Growth%',titlefont=dict(family='Calibri Light'))

        fig.append_trace(trace1,1,1)
        fig.append_trace(trace2,1,2)
        fig.append_trace(trace3,1,3)

        for i in fig['layout']['annotations']:
            i['font'] = dict(family='Calibri Light',size=15)

        fig['layout']['xaxis1'].update(showgrid=False,range=[-100,100],showticklabels=False)
        fig['layout']['xaxis2'].update(showgrid=False,range=[-100,100],showticklabels=False)
        fig['layout']['xaxis3'].update(showgrid=False,range=[-100,100],showticklabels=False)
        fig['layout']['yaxis1'].update(showgrid=False,autorange='reversed')
        return fig

########<Bubble Chart Callbacks>########
@app.callback(
    Output('bubble_chart','figure'),
    [Input('country','value'),
     Input('typeveh','value'),
     Input('channel','value'),]
)

def bubble_update(country_name,
                  typeveh_name,
                  channel_name):

    SQL="SELECT brands, tos, wdist, svper FROM bubble WHERE country=(%s) AND typeveh=(%s) AND channel=(%s)"
    cur.execute(SQL,(country_name,typeveh_name,channel_name,))
    result=cur.fetchall()
    brands_val, tos_val, wdist_val, svper_val = zip(*result)

    y1=np.array(brands_val)
    print(str(y1))
    color1=np.array(['rgba(255, 0, 0, 1)']*y1.shape[0])
    color1[y1=='SHELL']='rgb(255, 213, 0)'
    color1[y1=='ADNOC']='rgb(0, 102, 203)'
    color1[y1=='TOTAL']='rgb(84, 84, 169)'
    color1[y1=='CALTEX']='rgb(1, 129, 129)'
    color1[y1=='ENOC']='rgb(135, 8, 135)'
    color1[y1=='TOYOTA']='rgb(160, 212, 255)'
    color1[y1=='CASTROL']='rgb(255, 0, 0)'
    color1[y1=='LEXUS']='rgb(246, 202, 154)'
    color1[y1=='ZIC']='rgb(6, 204, 104)'
    color1[y1=='AC DELCO']='rgb(133, 47, 226)'
    color1[y1=='VOLVO']='rgb(247, 189, 155)'
    color1[y1=='VALVOLINE']='rgb(135, 135, 7)'
    color1[y1=='GULF']='rgb(2, 255, 2)'
    color1[y1=='AXCL']='rgb(0, 0, 255)'
    color1[y1=='NISSAN']='rgb(248, 191, 157)'

    trace1 = go.Scatter(x=wdist_val,y=tos_val,mode='markers',marker=dict(color=color1.tolist(),size=svper_val,),text=brands_val)
    fig = tls.make_subplots(rows=1, cols=1)
    fig.append_trace(trace1,1,1)
    fig['layout'].update(plot_bgcolor='#EFECEA',title='TOS Value vs W.Dist - Q2 2018',titlefont=dict(family='Calibri Light'))
    fig['layout']['xaxis1'].update(zeroline=False,gridcolor='#FFFFFF',ticks='outside',title='Weighted Distribution',titlefont=dict(family='Calibri Light'))
    fig['layout']['yaxis1'].update(zeroline=False,gridcolor='#FFFFFF',ticks='outside',title='TOS Value',titlefont=dict(family='Calibri Light'))
    return fig
