#!/usr/bin/python3
"""
route for handling place and amenities linking
"""
from flask import jsonify, abort
from os import getenv

from api.v1.views import app_views, storage


@app_views.route("/places/<place_id>/amenities",
                 methods=["GET"],
                 strict_slashes=False)
def amenity_by_place(place_id):
    """
    get all amenities of a place
    :param place_id: place id
    :return: all amenities
    """
    place = storage.get("Place", str(place_id))

    if place is None:
        abort(404)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get("Amenity", amenity_id).to_dict(
        ) for amenity_id in place.amenity_ids]

    return jsonify(amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def unlink_amenity_from_place(place_id, amenity_id):
    """
    unlinks an amenity in a place
    :param place_id: place id
    :param amenity_id: amenity id
    :return: empty dict or error
    """
    place = storage.get("Place", str(place_id))
    if place is None:
        abort(404)

    amenity = storage.get("Amenity", str(amenity_id))
    if amenity is None:
        abort(404)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)

    place.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"],
                 strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """
    links a amenity with a place
    :param place_id: place id
    :param amenity_id: amenity id
    :return: return Amenity obj added or error
    """
    place = storage.get("Place", str(place_id))
    if place is None:
        abort(404)

    amenity = storage.get("Amenity", str(amenity_id))
    if amenity is None:
        abort(404)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)

    place.save()
    return jsonify(amenity.to_dict()), 201
