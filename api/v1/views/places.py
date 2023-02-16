#!/usr/bin/python3
""" Module for Cities object related action/view"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage

from models.city import City
from models.user import User
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places_of_city(city_id):
    """ retrieves the list of all Place in a City objects """
    city = storage.get(City,  city_id)
    if not city:
        abort(404)

    lst = []
    for obj in city.places:
        lst.append(obj.to_dict())
    return jsonify(lst)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place_detail(place_id):
    """ Retrieves details of a Place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object """
    place_inst = storage.get(Place, place_id)
    if not place_inst:
        abort(404)

    storage.delete(place_inst)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Creates a new Place object """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    if "user_id" not in data:
        abort(400, "Missing user_id")

    user_id = data["user_id"]
    if not storage.get(User, user_id):
        abort(404)

    if "name" not in data:
        abort(400, "Missing name")

    new_place = Place(**data)
    setattr(new_place, 'city_id', city_id)
    storage.new(new_place)
    storage.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Update existing Place object """
    place_inst = storage.get(Place, place_id)
    if not place_inst:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    for key, val in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place_inst, key, val)

    storage.save()
    return make_response(jsonify(place_inst.to_dict()), 200)
