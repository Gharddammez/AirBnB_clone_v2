#!/usr/bin/python3
"""
Script that starts a Flask web application
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """
    Method to handle teardown of SQLAlchemy Session
    """
    storage.close()


@app.route('/states', strict_slashes=False)
def display_states():
    """
    Display a HTML page with the list of all State objects
    """
    states = storage.all(State).values()
    return render_template('9-states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def display_state_cities(id):
    """
    Display a HTML page with the list of City objects linked to the State
    """
    state = storage.get(State, id)
    if state is None:
        return render_template('9-states.html', not_found=True)
    else:
        return render_template('9-states.html', state=state)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
