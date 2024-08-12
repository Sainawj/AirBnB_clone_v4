#!/usr/bin/python3
"""
Flask routes for handling amenities in JSON format.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, CNC
from flasgger.utils import swag_from

@app_views.route('/amenities/', methods=['GET', 'POST'])
@swag_from('swagger_yaml/amenities_no_id.yml', methods=['GET', 'POST'])
def amenities_no_id():
    """
    Handle GET and POST requests for amenities when no specific ID is provided.
    - GET: Returns a list of all amenities in JSON format.
    - POST: Creates a new amenity from JSON data and returns the created amenity.
    """
    if request.method == 'GET':
        amenities = storage.all('Amenity')
        amenities_json = [obj.to_json() for obj in amenities.values()]
        return jsonify(amenities_json)

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if 'name' not in req_json:
            abort(400, 'Missing name')
        Amenity = CNC.get('Amenity')
        new_amenity = Amenity(**req_json)
        new_amenity.save()
        return jsonify(new_amenity.to_json()), 201

@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
@swag_from('swagger_yaml/amenities_id.yml', methods=['GET', 'DELETE', 'PUT'])
def amenities_with_id(amenity_id):
    """
    Handle GET, DELETE, and PUT requests for a specific amenity identified by its ID.
    - GET: Returns the amenity with the specified ID in JSON format.
    - DELETE: Deletes the amenity with the specified ID.
    - PUT: Updates the amenity with the specified ID using the provided JSON data.
    """
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(amenity.to_json())

    if request.method == 'DELETE':
        amenity.delete()
        return jsonify({}), 200

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        amenity.bm_update(req_json)
        return jsonify(amenity.to_json()), 200
