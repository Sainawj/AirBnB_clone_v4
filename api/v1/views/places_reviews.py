#!/usr/bin/python3
"""
Flask routes for handling reviews related to places.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from flasgger.utils import swag_from
from models import storage, CNC


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
@swag_from('swagger_yaml/reviews_by_place.yml', methods=['GET', 'POST'])
def reviews_per_place(place_id=None):
    """
    Handle GET and POST requests for reviews associated with a specific place.
    - GET: Returns a list of reviews for the specified place.
    - POST: Creates a new review for the specified place.
    """
    place_obj = storage.get('Place', place_id)

    if request.method == 'GET':
        if place_obj is None:
            abort(404, 'Place not found')
        all_reviews = storage.all('Review')
        place_reviews = [obj.to_json() for obj in all_reviews.values() if obj.place_id == place_id]
        return jsonify(place_reviews)

    if request.method == 'POST':
        if place_obj is None:
            abort(404, 'Place not found')
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        user_id = req_json.get("user_id")
        if user_id is None:
            abort(400, 'Missing user_id')
        user_obj = storage.get('User', user_id)
        if user_obj is None:
            abort(404, 'User not found')
        if req_json.get('text') is None:
            abort(400, 'Missing text')
        Review = CNC.get("Review")
        req_json['place_id'] = place_id
        new_review = Review(**req_json)
        new_review.save()
        return jsonify(new_review.to_json()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
@swag_from('swagger_yaml/reviews_id.yml', methods=['GET', 'DELETE', 'PUT'])
def reviews_with_id(review_id=None):
    """
    Handle GET, DELETE, and PUT requests for a specific review by ID.
    - GET: Returns the review with the specified ID.
    - DELETE: Deletes the review with the specified ID.
    - PUT: Updates the review with the specified ID.
    """
    review_obj = storage.get('Review', review_id)

    if request.method == 'GET':
        if review_obj is None:
            abort(404, 'Review not found')
        return jsonify(review_obj.to_json())

    if request.method == 'DELETE':
        if review_obj is None:
            abort(404, 'Review not found')
        review_obj.delete()
        return jsonify({}), 200

    if request.method == 'PUT':
        if review_obj is None:
            abort(404, 'Review not found')
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        review_obj.bm_update(req_json)
        return jsonify(review_obj.to_json()), 200
