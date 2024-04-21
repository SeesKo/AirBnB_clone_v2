#!/usr/bin/python3
"""Script that starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place


app = Flask(__name__)


@app.route('/hbnb')
def display_site():
    """Displays the Airbnb clone site"""
    states = storage.all(classes["State"]).values()
    amenities = storage.all(classes["Amenity"]).values()
    places = storage.all(classes["Place"]).values()

    # Sort data by name for consistent display
    states = sorted(states, key=lambda s: s.name)
    amenities = sorted(amenities, key=lambda a: a.name)
    places = sorted(places, key=lambda p: p.name)

    return render_template(
        '100-hbnb.html', states=states,
        amenities=amenities, places=places
    )


@app.teardown_appcontext
def teardown_db(exception):
    """Closes the storage after each request to avoid memory leaks"""
    storage.close()

if __name__ == "__main__":
    app.url_map.strict_slashes = False
    app.run(host="0.0.0.0", port=5000)
