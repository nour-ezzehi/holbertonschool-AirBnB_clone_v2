#!/usr/bin/python3
"""a script that starts a Flask web application"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity


app = Flask(__name__)
storage.all()


@app.teardown_appcontext
def teardown_data(self):
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def filter(id=None):
    data = storage.all(State)
    states = list()
    for state_instance in data.values():
        states.append(state_instance)

    data = storage.all(Amenity)
    amenities = list()
    for state_instance in data.values():
        amenities.append(state_instance)

    return render_template('10-hbnb_filters.html', states=states,
                           amenities=amenities)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
