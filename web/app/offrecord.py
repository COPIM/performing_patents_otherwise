# @name: offrecord.py
# @creation_date: 2022-10-27
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: offrecord route for Section 4: Off the record
# @acknowledgements:

from flask import Blueprint, render_template
import markdown

offrecord = Blueprint('offrecord', __name__)

# route for Martha Gowans page
@offrecord.route('/offrecord/')
def index():
    with open('content/section_4/I-Martha-gowans.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)
    return render_template('text.html', text=text)