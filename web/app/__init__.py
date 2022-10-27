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

    # blueprint for main parts of app (contents and frontmatter)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for search parts of app (Section 1: Searching the archive)
    from .search import search as search_blueprint
    app.register_blueprint(search_blueprint)

    # blueprint for interventions parts of app (Section 2: Search Interventions)
    from .interventions import interventions as interventions_blueprint
    app.register_blueprint(interventions_blueprint)

    # blueprint for hidden parts of app (Section 3: Hidden in plain sight)
    from .hidden import hidden as hidden_blueprint
    app.register_blueprint(hidden_blueprint)

    # blueprint for offrecord parts of app (Section 4: Off the record)
    from .offrecord import offrecord as offrecord_blueprint
    app.register_blueprint(offrecord_blueprint)

    # blueprint for making parts of app (Section 5: Making of)
    from .making import making as making_blueprint
    app.register_blueprint(making_blueprint)

    # blueprint for data parts of app
    from .data import data as data_blueprint
    app.register_blueprint(data_blueprint)

    return app
