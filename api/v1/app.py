#!/usr/bin/python3
""" Creates an app instance """

from api.v1.views import app_views
from flask import Flask
from os import getenv
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_session(exception):
    """teardown session"""
    storage.close()


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')

    if not host and not port:
        host = '0.0.0.0'
        port = 5000

    app.run(host=host, port=port, threaded=True)
