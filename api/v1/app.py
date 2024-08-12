#!/usr/bin/python3
"""
Flask application integrating with AirBnB static HTML templates.
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from flasgger import Swagger
from models import storage
import os
from werkzeug.exceptions import HTTPException

# Initialize Flask application
app = Flask(__name__)
swagger = Swagger(app)

# Disable strict slashes for cleaner URL handling
app.url_map.strict_slashes = False

# Configure server host and port from environment variables
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5001)

# Enable Cross-Origin Resource Sharing (CORS) for all origins on API routes
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Register application blueprint from api.v1.views
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_db(exception):
    """
    Close SQLAlchemy session after each request.
    """
    storage.close()

@app.errorhandler(404)
def handle_404(exception):
    """
    Handle 404 errors with a custom message.
    """
    code = 404
    description = "Resource not found"
    message = {'error': description}
    return make_response(jsonify(message), code)

@app.errorhandler(400)
def handle_400(exception):
    """
    Handle 400 errors with a custom message.
    """
    code = 400
    description = "Bad request"
    message = {'error': description}
    return make_response(jsonify(message), code)

@app.errorhandler(Exception)
def global_error_handler(err):
    """
    Handle all other exceptions globally.
    """
    if isinstance(err, HTTPException):
        code = err.code
        message = {'error': err.description}
    else:
        code = 500
        message = {'error': str(err)}
    return make_response(jsonify(message), code)

def setup_global_errors():
    """
    Register custom error handler for all HTTPException subclasses.
    """
    for cls in HTTPException.__subclasses__():
        app.register_error_handler(cls, global_error_handler)

if __name__ == "__main__":
    """
    Main entry point for the Flask application.
    """
    setup_global_errors()  # Initialize global error handling
    app.run(host=host, port=port)  # Start Flask application
