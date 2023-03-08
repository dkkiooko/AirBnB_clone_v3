#!/usr/bin/python3
"""
A new view for city object that handles all RESTful API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """ Gets the citiy objects of a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    list_cities = []
    for city in state.cities:
        list_cities.append(city.to_dict())

    return jsonify(list_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ Gets a city objects based on id """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def city_delete(city_id):
    """ Deletes the city with a given city_id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def city_post(state_id):
    """ Adds new city to database"""
    if not request.get_json():
        return make_response('Not a JSON', 400)
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if 'name' not in data.keys():
        return make_response('Missing name', 400)
    city = City(**data)
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def city_put(city_id):
    """ update city in database """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        return make_response('Not a JSON', 400)
    for key, val in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, val)
    storage.save()
    return jsonify(city.to_dict()), 200
