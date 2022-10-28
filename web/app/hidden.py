# @name: hidden.py
# @creation_date: 2022-10-27
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: hidden route for Section 3: Hidden in plain sight
# @acknowledgements:

from flask import Blueprint, render_template
from . import solr
import markdown

hidden = Blueprint('hidden', __name__)

# route for hidden page
@hidden.route('/hidden/')
def index():
    return render_template('index.html')

# route for active theme page
@hidden.route('/hidden/active/')
def active():
    with open('content/section_3/active.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)

    results = solr.get_number_random_records('active', 10)

    return render_template('theme.html', text=text, results=results)

# route for self-defending theme page
@hidden.route('/hidden/defending/')
def defending():
    with open('content/section_3/defending.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)

    results = solr.get_number_random_records('defending', 10)

    return render_template('theme.html', text=text, results=results)

# route for expanding theme page
@hidden.route('/hidden/expanding/')
def expanding():
    with open('content/section_3/expanding.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)

    results = solr.get_number_random_records('expanding', 10)

    return render_template('theme.html', text=text, results=results)

# route for invisible theme page
@hidden.route('/hidden/invisible/')
def invisible():
    with open('content/section_3/invisible.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)

    results = solr.get_number_random_records('invisible', 10)

    return render_template('theme.html', text=text, results=results)

# route for multispecies theme page
@hidden.route('/hidden/multispecies/')
def multispecies():
    with open('content/section_3/multispecies.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)

    results = solr.get_number_random_records('multispecies', 10)

    return render_template('theme.html', text=text, results=results)

# route for pissing theme page
@hidden.route('/hidden/pissing/')
def pissing():
    with open('content/section_3/pissing.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)

    results = solr.get_number_random_records('pissing', 10)

    return render_template('theme.html', text=text, results=results)

# route for secret theme page
@hidden.route('/hidden/secret/')
def secret():
    with open('content/section_3/secret.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)

    results = solr.get_number_random_records('secret', 10)

    return render_template('theme.html', text=text, results=results)

# route for surviving theme page
@hidden.route('/hidden/surviving/')
def surviving():
    with open('content/section_3/surviving.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)

    results = solr.get_number_random_records('surviving', 10)

    return render_template('theme.html', text=text, results=results)

# route for working theme page
@hidden.route('/hidden/working/')
def working():
    with open('content/section_3/working.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)

    results = solr.get_number_random_records('working', 10)

    return render_template('theme.html', text=text, results=results)
