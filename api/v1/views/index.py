#!/usr/bin/python3
""" imports app views """
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def status_response():
    """ Shows status response OK"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def stats():
    """ Route that counts and returns JSON"""
    list_of = {
            "amenities": Amenity,
            "cities": City,
            "places": Place,
            "reviews": Review,
            "states": State,
            "users": User
        }
    result = {}

    for key, value in list_of.items():
        result[key] = storage.count(value)
    return jsonify(result)
