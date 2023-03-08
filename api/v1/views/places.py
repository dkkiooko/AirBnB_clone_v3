#!/usr/bin/python3
"""
A new view for place object that handles all RESTful API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """ Gets the place objects of a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    list_places = []
    for place in city.places:
        list_places.append(place.to_dict())

    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Gets a place objects based on id """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def place_delete(place_id):
    """ Deletes the place with a given Place_id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def place_post(city_id):
    """ Adds new place to database"""
    if not request.get_json():
        return make_response('Not a JSON', 400)
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    data = request.get_json()

    if 'name' not in data.keys():
        return make_response('Missing name', 400)
    if 'user_id' not in data.keys():
        return make_response('Missing user_id', 400)

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    place = Place(**data)
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def place_put(place_id):
    """ update place in database """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        return make_response('Not a JSON', 400)
    for key, val in data.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, val)
    storage.save()
    return jsonify(place.to_dict()), 200
