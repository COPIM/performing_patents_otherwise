# @name: hidden.py
# @creation_date: 2022-10-27
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: hidden route for Section 3: Hidden in plain sight
# @acknowledgements:

from flask import Blueprint, render_template
import markdown

hidden = Blueprint('hidden', __name__)

# route for hidden page
@hidden.route('/hidden/')
def index():
    return render_template('index.html')

# route for active theme page
@hidden.route('/hidden/active/')
def active():
    return render_template('index.html')
