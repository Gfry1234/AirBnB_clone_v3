#!/usr/bin/python3
""" Module for States object related action/view"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """ retrieves the list of all State objects """
    states = storage.all(State)
    lst = []
    for obj in states.values():
        lst.append(obj.to_dict())
    return jsonify(lst)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_detail(state_id):
    """ Retrieves details of a State """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Deletes a State object """
    state_inst = storage.get(State, state_id)
    if not state_inst:
        abort(404)

    storage.delete(state_inst)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Creates a new State object """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    if "name" not in data:
        abort(400, "Missing name")

    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Update existing State object """
    state_inst = storage.get(State, state_id)
    if not state_inst:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    for key, val in data.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(state_inst, key, val)

    storage.save()
    return make_response(jsonify(state_inst.to_dict()), 200)
