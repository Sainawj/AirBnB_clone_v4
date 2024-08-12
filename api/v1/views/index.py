#!/usr/bin/python3
"""
Flask routes for status and statistics in JSON format.
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    Return a JSON response with the status of the API.
    - GET: Returns a JSON object with the status set to 'OK'.
    """
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'])
def stats():
    """
    Return a JSON response with counts of all class objects.
    - GET: Returns a JSON object where each key is a resource name
      and each value is the count of that resource in the database.
    """
    response = {}
    PLURALS = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
    }
    for key, value in PLURALS.items():
        response[value] = storage.count(key)
    return jsonify(response)
