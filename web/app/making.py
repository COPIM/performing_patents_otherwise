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

# route for interface design essay
@making.route('/making/interface/')
def interface():
    with open('content/section_5/on-interface-design.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)
    return render_template('text.html', text=text)

# route for databases essay
@making.route('/making/databases/')
def databases():
    with open('content/section_5/on-combining-databases-and-books.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)
    return render_template('text.html', text=text)