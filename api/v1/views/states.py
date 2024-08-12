#!/usr/bin/python3
"""
Flask routes for handling state-related requests.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from flasgger import swag_from
from models import storage, CNC


@app_views.route('/states', methods=['GET', 'POST'])
@swag_from('swagger_yaml/states_no_id.yml', methods=['GET', 'POST'])
def states_no_id():
    """
    Handle GET and POST requests for states without specifying an ID.
    - GET: Returns a list of all states.
    - POST: Creates a new state with the provided data.
    """
    if request.method == 'GET':
        all_states = storage.all('State')
        states_list = [obj.to_json() for obj in all_states.values()]
        return jsonify(states_list)

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if req_json.get("name") is None:
            abort(400, 'Missing name')
        State = CNC.get("State")
        new_state = State(**req_json)
        new_state.save()
        return jsonify(new_state.to_json()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
@swag_from('swagger_yaml/states_id.yml', methods=['GET', 'DELETE', 'PUT'])
def states_with_id(state_id=None):
    """
    Handle GET, DELETE, and PUT requests for a specific state by ID.
    - GET: Returns the state with the specified ID.
    - DELETE: Deletes the state with the specified ID.
    - PUT: Updates the state with the specified ID.
    """
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404, 'State not found')

    if request.method == 'GET':
        return jsonify(state_obj.to_json())

    if request.method == 'DELETE':
        state_obj.delete()
        return jsonify({}), 200

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        state_obj.bm_update(req_json)
        return jsonify(state_obj.to_json()), 200
