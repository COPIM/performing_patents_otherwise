# @name: offrecord.py
# @creation_date: 2022-10-27
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: offrecord route for Section 4: Off the record
# @acknowledgements:

from flask import Blueprint, render_template
import markdown

offrecord = Blueprint('offrecord', __name__)

# route for off the record page
@offrecord.route('/offrecord/')
def index():
    return render_template('index.html')
