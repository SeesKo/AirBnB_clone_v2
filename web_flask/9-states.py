#!/usr/bin/python3
""" Script that starts a Flask web application """
from flask import Flask, request, render_template
from models import storage
from models.city import City
from models.state import State


app = Flask(__name__)


@app.route("/states", strict_slashes=False)
@app.route("/states/<id>", strict_slashes=False)
def states_id(id=None):
    """ Renders all states or a specific state based on the given ID """
    states = storage.all(State)
    if id is None:
        return render_template(
            "9-states.html", states=states
        )
    else:
        return render_template(
            "9-states.html", states=states,
            id="State." + id
        )


@app.teardown_appcontext
def remove_session(exception):
    """
    Closes the storage session at the end of the app context,
    regardless of exceptions
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
