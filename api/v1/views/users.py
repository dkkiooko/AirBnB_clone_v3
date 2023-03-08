#!/usr/bin/python3
"""
A new view for User object that handles all RESTful API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User


@app_views.route('/users/', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_users(user_id=None):
    """ Gets the user object with user_id"""
    list_users = []
    if user_id is None:
        for user in storage.all(User).values():
            list_users.append(user.to_dict())
        return jsonify(list_users)
    else:
        user = storage.get(User, user_id)
        if not user:
            abort(404)
        return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def user_delete(user_id):
    """ Deletes the user with a given user_id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def user_post():
    """ Adds new user to database"""
    if not request.get_json():
        return make_response('Not a JSON', 400)
    data = request.get_json()
    if 'email' not in data.keys():
        return make_response('Missing email', 400)
    if 'password' not in data.keys():
        return make_response('Missing password', 400)
    user = User(**data)
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def user_put(user_id):
    """ replace user in database """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data = request.get_json()
    if not data:
        return make_response('Not a JSON', 400)
    for key, val in data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, val)
    storage.save()
    return jsonify(user.to_dict()), 200
