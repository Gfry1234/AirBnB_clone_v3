#!/usr/bin/python3
""" Module for Cities object related action/view"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage

from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities_of_state(state_id):
    """ retrieves the list of all Cities objects """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    lst = []
    for obj in state.cities:
        lst.append(obj.to_dict())
    return jsonify(lst)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_detail(city_id):
    """ Retrieves details of a City """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Deletes a City object """
    city_inst = storage.get(City, city_id)
    if not city_inst:
        abort(404)

    storage.delete(city_inst)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ Creates a new City object """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    if "name" not in data:
        abort(400, "Missing name")

    new_city = City(**data)
    setattr(new_city, 'state_id', state_id)
    storage.new(new_city)
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ Update existing City object """
    city_inst = storage.get(City, city_id)
    if not city_inst:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    for key, val in data.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(city_inst, key, val)

    storage.save()
    return make_response(jsonify(city_inst.to_dict()), 200)
