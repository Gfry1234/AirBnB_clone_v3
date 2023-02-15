#!/usr/bin/python3
""" Landing/Index Page """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """ Returns jsonified status """
    return jsonify(status="OK")
