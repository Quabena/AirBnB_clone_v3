#!/usr/bin/python3
'''Contains the states view for the API.'''
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    return jsonify([state.to_dict() for state in storage.all(State).values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object by ID"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object by ID"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    storage.delete(obj)  # Correct method to delete
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new State object"""
    try:
        new_obj = request.get_json()
        if not isinstance(new_obj, dict):  # Ensure it's a dictionary
            abort(400, description="Not a JSON")
    except Exception:
        abort(400, description="Not a JSON")

    if 'name' not in new_obj or not isinstance(new_obj['name'], str):
        abort(400, description="Missing name")

    obj = State(**new_obj)
    storage.new(obj)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)

    try:
        req = request.get_json()
        if not isinstance(req, dict):
            abort(400, description="Not a JSON")
    except Exception:
        abort(400, description="Not a JSON")

    ignored_keys = {'id', 'created_at', 'updated_at'}

    for key, value in req.items():
        if key not in ignored_keys and isinstance(
                value, (str, int, float, bool)):
            setattr(obj, key, value)

    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)
