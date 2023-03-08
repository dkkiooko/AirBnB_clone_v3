#!/usr/bin/python3
"""
A new view for city object that handles all RESTful API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """ Gets the reviews of a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    list_reviews = []
    for review in place.reviews:
        list_reviews.append(review.to_dict())

    return jsonify(list_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """ Gets a review objects based on id """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def review_delete(review_id):
    """ Deletes the review based on id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def review_post(place_id):
    """ Adds new place review to database"""
    if not request.get_json():
        return make_response('Not a JSON', 400)
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if 'text' not in data.keys():
        return make_response("Missing text", 400)
    if 'user_id' not in data.keys():
        return make_response('Missing user_id', 400)
    user = storage.get(User, data['user_id'])
    if not user:
        return abort(404)
    review = Review(**data)
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def review_put(review_id):
    """ update review in database """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    data = request.get_json()
    if not data:
        return make_response('Not a JSON', 400)
    for key, val in data.items():
        if key not in ["id", "user_id", "place_id", "created_at",
                       "updated_at"]:
            setattr(review, key, val)
    storage.save()
    return jsonify(review.to_dict()), 200
