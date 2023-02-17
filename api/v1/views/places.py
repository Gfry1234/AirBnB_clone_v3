#!/usr/bin/python3
""" Module for Cities object related action/view"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage

from models.amenity import Amenity
from models.city import City
from models.state import State
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


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """ retrieves all Place objects depending of
    the JSON in the body of the request.
    """
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    if not data or (not data.get('states') and not data.get('cities')
                    and not data.get('amenities')):
        places = storage.all(Place).values()
        lst = []
        for obj in places:
            lst.append(obj.to_dict())
        return jsonify(lst)

    list_places = []
    if data.get('states'):
        states = [storage.get(State, id) for id in data.get('states')]
        for state in states:
            for city in state.cities:
                for place in city.places:
                    list_places.append(place)

    if data.get('cities'):
        cities = [storage.get(City, id) for id in data.get('cities')]
        for city in cities:
            for place in city.places:
                if place not in list_places:
                    list_places.append(place)

    if data.get('amenities'):
        if not list_places:
            list_places = storage.all(Place).values()
        amenities = [storage.get(Amenity, id) for id in data.get('amenities')]
        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in amenities])]

    places = []
    for p in list_places:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)

    return jsonify(places)
