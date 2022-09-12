# @name: __init__.py
# @creation_date: 2022-09-07
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: Initialises the app, SQLAlchemy, and configuration variables
# @acknowledgements:
# https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login
# Config stuff adapted from https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms

from flask import Flask
from flask_moment import Moment
import os

# initiate Moment for datetime functions
moment = Moment()

def create_app():
    app = Flask(__name__)

    moment.init_app(app)

    # blueprint for main parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for search parts of app
    from .search import search as search_blueprint
    app.register_blueprint(search_blueprint)

    # blueprint for random parts of app
    from .random import random as random_blueprint
    app.register_blueprint(random_blueprint)

    return app
