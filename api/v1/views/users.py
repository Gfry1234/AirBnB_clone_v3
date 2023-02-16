#!/usr/bin/python3
""" Module for Cities object related action/view"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage

from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """ retrieves the list of all User objects """
    users = storage.all(User)
    lst = []
    for obj in users.values():
        lst.append(obj.to_dict())
    return jsonify(lst)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_detail(user_id):
    """ Retrieves details of a User """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User object """
    user_inst = storage.get(User, user_id)
    if not user_inst:
        abort(404)

    storage.delete(user_inst)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Creates a new User object """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    if "email" not in data:
        abort(400, "Missing name")

    if "password" not in data:
        abort(400, "Missing password")

    new_user = User(**data)
    storage.new(new_user)
    storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_city(user_id):
    """ Update existing User object """
    user_inst = storage.get(User, user_id)
    if not user_inst:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    for key, val in data.items():
        if key != 'id' and key != 'email' and key != 'created_at' \
                and key != 'updated_at':
            setattr(user_inst, key, val)

    storage.save()
    return make_response(jsonify(user_inst.to_dict()), 200)
