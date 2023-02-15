#!/usr/bin/python3
""" Landing/Index Page """
from api.v1.views import app_views
from flask import jsonify

import models
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {
        "Amenity": Amenity, "City": City, "Place": Place,
        "Review": Review, "State": State, "User": User}


@app_views.route('/status', methods=['GET'])
def status():
    """ Returns jsonified status """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def some_stats():
    """ retrieves the number of each objects by type
    """
    num_obj = {}
    for obj in classes:
        num_obj["{}".format(obj.lower())] = models.storage.count(obj)
    return jsonify(num_obj)
