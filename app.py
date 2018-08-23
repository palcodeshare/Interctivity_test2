import dash
import os

from flask import send_from_directory


app = dash.Dash(__name__)
server=app.server
server.secret_key = os.environ.get('secret_key', 'secret')
app.config.supress_callback_exceptions = True

external_css = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    '/static/base.css'
]
for css in external_css:
    app.css.append_css({"external_url": css})


@app.server.route('/static/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)
