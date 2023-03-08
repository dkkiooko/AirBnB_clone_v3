#!/usr/bin/python3
"""
A new view for city object that handles all RESTful API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ Gets the amenities in storage """
    amenities = []
    for amenity in storage.all(Amenity).values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ Gets a amenity objects based on id """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def amenity_delete(amenity_id):
    """ Deletes the amenity with a given amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/amenities/', methods=['POST'], strict_slashes=False)
def amenity_post():
    """ create an amenity """
    if not request.get_json():
        return make_response('Not a JSON', 400)
    data = request.get_json()
    if 'name' not in data.keys():
        return make_response('Missing name', 400)
    amenity = Amenity(**data)
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def amenity_put(amenity_id):
    """ update amenity in database """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    data = request.get_json()
    if not data:
        return make_response('Not a JSON', 400)
    for key, val in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, val)
    storage.save()
    return jsonify(amenity.to_dict()), 200
