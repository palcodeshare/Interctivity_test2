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

app = dash.Dash('auth')
auth = dash_auth.BasicAuth(
    app,
    (('gfkdxb','1234',),)
)

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
cur.execute("SELECT DISTINCT(region) FROM react_table")
region1=cur.fetchall()
reg_val = [sales[0] for sales in region1]

#Auth





#Dash app

app = dash.Dash('app',server=server)

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

        dcc.Graph(id='react-graph')
    ])
])

@app.callback(
    Output('react-graph','figure'),
    [Input('reg_col','value')]
)

def update_graph(reg_col_name):

    print(reg_col_name)
    SQL="SELECT fruits FROM react_table WHERE region = (%s)"
    cur.execute(SQL,(reg_col_name,))
    fruits1=cur.fetchall()
    fruits_val = [fruit[0] for fruit in fruits1]
    SQL1="SELECT sales FROM react_table WHERE region = (%s) "
    cur.execute(SQL1,(reg_col_name,))
    sales1=cur.fetchall()
    sales_val = [sales[0] for sales in sales1]
    print(sales_val)
    clo = conn.rollback()

    return {
        'data': [go.Bar(
            x=fruits_val, y=sales_val, name='SF'
        )]
    }

app.scripts.config.serve_locally = True
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

if __name__ == '__main__':
    app.run_server(debug=True)
