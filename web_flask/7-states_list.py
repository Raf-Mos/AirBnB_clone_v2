#!/usr/bin/python3
"""
starts a Flask web application
/states_list: display a HTML page
"""
from flask import Flask, render_template
from models import storage
from models import *
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """
    /states_list: display a HTML page: (inside the tag BODY)
    """
    states = storage.all(State)

    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown(exception):
    """ Remove the current SQLAlchemy Session """
    return storage.close()


if __name__ == "__main__":
    """ Run the web app on 0.0.0.0 port 5000 """
    app.run(host='0.0.0.0', port=5000)
