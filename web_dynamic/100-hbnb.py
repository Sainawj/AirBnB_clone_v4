#!/usr/bin/python3
""" 
Starts a Flask Web Application to display HBNB data.
"""
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from flask import Flask, render_template
import uuid

# Initialize Flask application
app = Flask(__name__)

@app.teardown_appcontext
def close_db(error):
    """ 
    Closes the SQLAlchemy session after each request. 
    """
    storage.close()

@app.route('/100-hbnb/', strict_slashes=False)
def hbnb():
    """ 
    Renders the '100-hbnb.html' template with states, cities, amenities, and places data.
    """
    # Retrieve and sort states and cities
    states = storage.all(State).values()
    states = sorted(states, key=lambda state: state.name)
    st_ct = [[state, sorted(state.cities, key=lambda city: city.name)] for state in states]

    # Retrieve and sort amenities and places
    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda amenity: amenity.name)

    places = storage.all(Place).values()
    places = sorted(places, key=lambda place: place.name)
    
    # Generate a unique cache ID
    cache_id = uuid.uuid4()

    return render_template('100-hbnb.html',
                           states=st_ct,
                           amenities=amenities,
                           places=places,
                           cache_id=cache_id)

if __name__ == "__main__":
    """ 
    Run the Flask application on the specified host and port. 
    """
    app.run(host='0.0.0.0', port=5000)
