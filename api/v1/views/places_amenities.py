#!/usr/bin/python3
""" Module for Place-Amenity object related action/view"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response
from models import storage
from os import getenv

from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def amenities_of_place(place_id):
    """ retrieves the list of all Amenities for a Place objects """
    place = storage.get(Place,  place_id)
    if not place:
        abort(404)

    lst = []
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        for obj in place.amenities:
            lst.append(obj.to_dict())
    else:
        for id in place.amenity_ids:
            lst.append(storage.get(Amenity, id).to_dict())
    return jsonify(lst)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenities_place(place_id, amenity_id):
    """ Delete an Amenity object of Place Object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)

    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def create_amenities_place(place_id, amenity_id):
    """ Link a Amenity object to a Place Object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == "db":
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        place.amenity_ids.append(amenity_id)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
