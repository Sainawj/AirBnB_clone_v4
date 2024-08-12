#!/usr/bin/python3
"""
Flask App that integrates with AirBnB static HTML Template
"""
from flask import Flask, render_template
from models import storage
import uuid

# Flask app setup
app = Flask(__name__)
app.url_map.strict_slashes = False
port = 5000
host = '0.0.0.0'

@app.teardown_appcontext
def teardown_db(exception):
    """
    Closes the SQLAlchemy session after each request.
    """
    storage.close()

@app.route('/4-hbnb/')
def hbnb_filters():
    """
    Renders the '4-hbnb.html' template with states, cities, amenities, places,
    and users data. Generates a unique cache ID for cache busting.
    """
    # Retrieve all data from storage
    state_objs = storage.all('State').values()
    states = {state.id: state for state in state_objs}
    
    amens = storage.all('Amenity').values()
    places = storage.all('Place').values()
    users = {user.id: "{} {}".format(user.first_name, user.last_name)
             for user in storage.all('User').values()}
    
    # Generate a unique cache ID
    cache_id = uuid.uuid4()

    return render_template('4-hbnb.html',
                           states=states,
                           amens=amens,
                           places=places,
                           users=users,
                           cache_id=cache_id)

if __name__ == "__main__":
    """
    Run the Flask app on the specified host and port.
    """
    app.run(host=host, port=port)
