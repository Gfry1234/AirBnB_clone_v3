#!/usr/bin/python3
""" Module for Review object related action/view"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage

from models.user import User
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews_of_place(place_id):
    """ retrieves the list of all Reviews for a Place objects """
    place = storage.get(Place,  place_id)
    if not place:
        abort(404)

    lst = []
    for obj in place.reviews:
        lst.append(obj.to_dict())
    return jsonify(lst)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def review_detail(review_id):
    """ Retrieves details of a Review """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a Review object """
    review_inst = storage.get(Review, review_id)
    if not review_inst:
        abort(404)

    storage.delete(review_inst)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Creates a new Review object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    if "user_id" not in data:
        abort(400, "Missing user_id")

    user_id = data["user_id"]
    if not storage.get(User, user_id):
        abort(404)

    if "text" not in data:
        abort(400, "Missing text")

    new_review = Review(**data)
    setattr(new_review, 'place_id', place_id)
    storage.new(new_review)
    storage.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ Update existing Review object """
    review_inst = storage.get(Review, review_id)
    if not review_inst:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    for key, val in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(review_inst, key, val)

    storage.save()
    return make_response(jsonify(review_inst.to_dict()), 200)
