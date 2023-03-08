#!/usr/bin/python3
"""
A new view for state object that handles all RESTful API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states(state_id=None):
    """ Gets the state object with state_id"""
    list_states = []
    if state_id is None:
        for state in storage.all(State).values():
            list_states.append(state.to_dict())
        return jsonify(list_states)
    else:
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def state_delete(state_id):
    """ Deletes the state with a given state_id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def state_post():
    """ Adds new state to database"""
    if not request.get_json():
        return make_response('Not a JSON', 400)
    data = request.get_json()
    if 'name' not in data.keys():
        return make_response('Missing name', 400)
    state = State(**data)
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def state_put(state_id):
    """ replace state in database """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        return make_response('Not a JSON', 400)
    for key, val in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, val)
    storage.save()
    return jsonify(state.to_dict()), 200
