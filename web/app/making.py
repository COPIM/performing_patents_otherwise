# @name: making.py
# @creation_date: 2022-10-27
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: making route for Section 4: Making of
# @acknowledgements:

from flask import Blueprint, render_template
import markdown

making = Blueprint('making', __name__)

# route for making of page
@making.route('/making/')
def index():
    with open('content/section_3/making.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)
    return render_template('making-overview.html', text=text)

# route for interface design essay
@making.route('/making/interface/')
def interface():
    with open('content/section_3/on-interface-design.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)
    return render_template('text.html', text=text)

# route for databases essay
@making.route('/making/database-book/')
def databases():
    with open('content/section_3/on-combining-databases-and-books.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)
    return render_template('text.html', text=text)

# route for interview
@making.route('/making/interview/')
def interview():
    with open('content/section_3/making-of-interview.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)
    return render_template('text.html', text=text)