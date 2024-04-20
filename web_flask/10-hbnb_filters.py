#!/usr/bin/python3
""" Script that starts a Flask web application """
from flask import Flask, request, render_template
from models import storage
from models.amenity import Amenity
from models.state import State


app = Flask(__name__)


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filter():
    """ 
    Renders a page with filters for states and amenities
    """
    states = storage.all(State)
    amenities = storage.all(Amenity)
    return render_template(
        "10-hbnb_filters.html", states=states,
        amenities=amenities
    )


@app.teardown_appcontext
def remove_session(exception):
    """
    Closes current SQLAlchemy session after each request
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
