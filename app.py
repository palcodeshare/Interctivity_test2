from dash import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import psycopg2
import os
import flask

#Flask hosting
server = flask.Flask('app')
server.secret_key = os.environ.get('secret_key', 'secret')

#Database connection
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

#Queries
cur.execute("SELECT fruits FROM react_table ")
fruits1=cur.fetchall()
fruits_val = [fruit[0] for fruit in fruits1]
cur.execute("SELECT sales FROM react_table")
sales1=cur.fetchall()
sales_val = [sales[0] for sales in sales1]
cur.execute("SELECT region FROM react_table")
region1=cur.fetchall()
reg_val = [sales[0] for sales in region1]

#Dash app
app = dash.Dash()

app.layout = html.Div([
    html.Div([
        html.H1(
            children='Hello Dash'
        ),

        html.Div(
            children='''Dash: A web application framework for Python.'''
        ),

        dcc.Dropdown(
            id='reg_col',
            options=[{'label': i, 'value': i} for i in reg_val],
            value='Dubai'
        ),

        dcc.Graph(id='react-graph',
            figure=go.Figure(
                data=[
                    go.Bar(
                        x=fruits_val, y=sales_val, name='SF'
                    ),
                ],
            )
        )
    ])
])

@app.callback(
    dash.dependencies.Output('react-graph','figure'),
    [dash.dependencies.Input('reg_col','value')]
)

def update_graph(reg_col):

    cur.execute("SELECT fruits FROM react_table WHERE region = value ")
    fruits1=cur.fetchall()
    fruits_val = [fruit[0] for fruit in fruits1]
    cur.execute("SELECT sales FROM react_table WHERE region = value")
    sales1=cur.fetchall()
    sales_val = [sales[0] for sales in sales1]

    return {
        'data': [go.Bar(
            x=fruits_val, y=sales_val, name='SF'
        )]
    }

if __name__ == '__main__':
    app.run_server(debug=True)
