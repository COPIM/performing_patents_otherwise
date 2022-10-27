# @name: making.py
# @creation_date: 2022-10-27
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: making route for Section 5: Making of
# @acknowledgements:

from flask import Blueprint, render_template
import markdown

making = Blueprint('making', __name__)

# route for making of page
@making.route('/making/')
def index():
    return render_template('index.html')
