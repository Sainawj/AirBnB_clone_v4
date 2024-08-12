#!/usr/bin/python3
"""
Flask routes for handling user-related requests.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, CNC
from flasgger.utils import swag_from


@app_views.route('/users/', methods=['GET', 'POST'])
@swag_from('swagger_yaml/users_no_id.yml', methods=['GET', 'POST'])
def users_no_id():
    """
    Handle GET and POST requests for users without specifying an ID.
    - GET: Returns a list of all users.
    - POST: Creates a new user with the provided data.
    """
    if request.method == 'GET':
        all_users = storage.all('User')
        users_list = [obj.to_json() for obj in all_users.values()]
        return jsonify(users_list)

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if req_json.get('email') is None:
            abort(400, 'Missing email')
        if req_json.get('password') is None:
            abort(400, 'Missing password')
        User = CNC.get('User')
        new_user = User(**req_json)
        new_user.save()
        return jsonify(new_user.to_json()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
@swag_from('swagger_yaml/users_id.yml', methods=['GET', 'DELETE', 'PUT'])
def user_with_id(user_id=None):
    """
    Handle GET, DELETE, and PUT requests for a specific user by ID.
    - GET: Returns the user with the specified ID.
    - DELETE: Deletes the user with the specified ID.
    - PUT: Updates the user with the specified ID.
    """
    user_obj = storage.get('User', user_id)
    if user_obj is None:
        abort(404, 'User not found')

    if request.method == 'GET':
        return jsonify(user_obj.to_json())

    if request.method == 'DELETE':
        user_obj.delete()
        return jsonify({}), 200

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        user_obj.bm_update(req_json)
        return jsonify(user_obj.to_json()), 200
