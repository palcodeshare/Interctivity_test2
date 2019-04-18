import dash
import dash_auth
import os
#
# from flask import send_from_directory
from rq import Queue
from apps/worker import conn
from utils import count_words_at_url



q = Queue(connection=conn)
result = q.enqueue(count_words_at_url, 'http://heroku.com')

app = dash.Dash()
app.config.suppress_callback_exceptions = True
