#!/usr/bin/python3
""" Module for Cities object related action/view"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage

from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def all_amenities():
    """ retrieves the list of all Amenities objects """
    amenities = storage.all(Amenity)
    lst = []
    for obj in amenities.values():
        lst.append(obj.to_dict())
    return jsonify(lst)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity_detail(amenity_id):
    """ Retrieves details of an Amenity """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes an Amenity object """
    amenity_inst = storage.get(Amenity, amenity_id)
    if not amenity_inst:
        abort(404)

    storage.delete(amenity_inst)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """ Creates a new City object """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    if "name" not in data:
        abort(400, "Missing name")

    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Update existing Amenity object """
    amenity_inst = storage.get(Amenity, amenity_id)
    if not amenity_inst:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    for key, val in data.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(amenity_inst, key, val)

    storage.save()
    return make_response(jsonify(amenity_inst.to_dict()), 200)
