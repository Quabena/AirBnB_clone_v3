#!/usr/bin/python3
'''Contains the amenities view for the API.'''
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    """Retrieves the list of all Amenity objects"""
    objs = storage.all(Amenity)
    return jsonify([obj.to_dict() for obj in objs.values()])


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def single_amenities(amenity_id):
    """Retrieves an Amenity object"""
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404, description="Amenity not found")
    return jsonify(obj.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_amenities(amenity_id):
    """Deletes an Amenity object and returns an empty dictionary"""
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404, description="Amenity not found")

    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Creates a new Amenity and returns it with status code 201"""
    try:
        new_amenity = request.get_json()
        if not isinstance(new_amenity, dict):
            abort(400, "Not a JSON")
    except Exception:
        abort(400, "Not a JSON")

    if 'name' not in new_amenity:
        abort(400, "Missing name")

    if not isinstance(
            new_amenity['name'],
            str) or not new_amenity['name'].strip():
        abort(400, "Invalid name")

    obj = Amenity(**new_amenity)
    storage.new(obj)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """Updates an Amenity object and returns it"""
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404, description="Amenity not found")

    try:
        req = request.get_json()
        if not isinstance(req, dict):
            abort(400, "Not a JSON")
    except Exception:
        abort(400, "Not a JSON")

    for k, v in req.items():
        if k not in ['id', 'created_at', 'updated_at']:
            if k == 'name' and (not isinstance(v, str) or not v.strip()):
                abort(400, "Invalid name")
            setattr(obj, k, v)

    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)
