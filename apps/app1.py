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

#Bootstrap CSS
#app.css.append_css({'external_url': 'https://codepen.io/mokshaxkrodha/pen/XBXNbP'})

#app = dash.Dash('auth')
#auth = dash_auth.BasicAuth(
#    app,
#    (('abcd','1234',),)
#)



#Database connection
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

cur.execute("SELECT DISTINCT(region) FROM react_table")
region1=cur.fetchall()
reg_val = [sales[0] for sales in region1]

#Dash app

app = dash.Dash('app',server=server)

app.css.append_css({'external_url': 'https://codepen.io/mokshaxkrodha/pen/XBXNbP'})

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1(
                children='GfK Dashboard Application'
            ),

            html.H4(
                children='''Shell Dashboard'''
            )
        ], className = "ten columns"),

        html.Div([
            html.Img(
                src="https://image.ibb.co/iZDuHT/Webp_net_resizeimage_1.png"
            )
        ], className = "one columns"),


        html.Div([
            html.Img(
                src="https://www.gfk.com/fileadmin/fe/gfktheme/images/favicons/apple-touch-icon-72x72.png"
            )
        ], className = "one columns")

    ], className = "row"),

    html.Div([
        html.Div([
            dcc.Graph(id='react-graph'),

            dcc.Dropdown(
                id='reg_col',
                options=[{'label': i, 'value': i} for i in reg_val],
                value='Dubai'
            )
        ], className = "six columns")
    ], className = "row")
])

@app.callback(
    Output('react-graph','figure'),
    [Input('reg_col','value')]
)

def update_graph(reg_col_name):

    SQL="SELECT fruits, sales FROM react_table WHERE region = (%s)"
    cur.execute(SQL,(reg_col_name,))
    result=cur.fetchall()
    fruits_val, sales_val = zip(*result)

    return {
        'data': [go.Bar(
            x=fruits_val, y=sales_val, name='SF'
        )]
    }

app.scripts.config.serve_locally = True
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

if __name__ == '__main__':
    app.run_server(debug=True)
