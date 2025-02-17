#!/usr/bin/python3
"""
Route for handling the linking between Place and Amenity objects.
This module provides endpoints to list, link, and unlink Amenity objects
to/from a Place object, depending on the storage
type (DBStorage or FileStorage).
"""

from flask import jsonify, abort
from os import getenv

from api.v1.views import app_views, storage


@app_views.route("/places/<place_id>/amenities", methods=["GET"], strict_slashes=False)
def amenity_by_place(place_id):
    """
    Retrieves the list of all Amenity objects associated
    with a Place.

    Args:
        place_id (str): The ID of the Place object.

    Returns:
        JSON: A list of Amenity objects in JSON format.
        Error: 404 if the Place object is not found.
    """
    place = storage.get("Place", str(place_id))

    if place is None:
        abort(404)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get("Amenity", amenity_id).to_dict() for amenity_id in place.amenity_ids]

    return jsonify(amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["DELETE"], strict_slashes=False)
def unlink_amenity_from_place(place_id, amenity_id):
    """
    Unlinks an Amenity object from a Place object.

    Args:
        place_id (str): The ID of the Place object.
        amenity_id (str): The ID of the Amenity object.

    Returns:
        JSON: An empty dictionary with status code 200.
        Error: 404 if the Place or Amenity object is not found,
               or if the Amenity is not linked to the Place.
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


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"], strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """
    Links an Amenity object to a Place object.

    Args:
        place_id (str): The ID of the Place object.
        amenity_id (str): The ID of the Amenity object.

    Returns:
        JSON: The linked Amenity object in JSON format.
        Error: 404 if the Place or Amenity object is not found.
               Returns the Amenity object with status code 200 if already linked.
               Returns the Amenity object with status code 201 if newly linked.
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
