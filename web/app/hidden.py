# @name: hidden.py
# @creation_date: 2022-10-27
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: hidden route for Section 2: Hidden in plain sight
# @acknowledgements:

from flask import Blueprint, render_template
from . import solr
import markdown

hidden = Blueprint('hidden', __name__)

# route for hidden page
@hidden.route('/hidden/')
def index():
    with open('content/hidden/intro-hidden.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)
    return render_template('hidden.html', text=text)

# route for expanding theme page
@hidden.route('/hidden/expanding/')
def expanding():
    core = 'expanding'
    with open('content/hidden/expanding.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)

    results = solr.get_number_random_records(core, 10)

    return render_template('theme.html', text=text, results=results, core=core)

# route for active theme page
@hidden.route('/hidden/active/')
def active():
    core = 'active'
    with open('content/hidden/active.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)

    results = solr.get_number_random_records(core, 10)

    return render_template('theme.html', text=text, results=results, core=core)

# route for secret theme page
@hidden.route('/hidden/secret/')
def secret():
    core = 'secret'
    with open('content/hidden/secret.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)

    results = solr.get_number_random_records(core, 10)

    return render_template('theme.html', text=text, results=results, core=core)

# route for leaking theme page
@hidden.route('/hidden/leaking/')
def leaking():
    core = 'leaking'
    with open('content/hidden/leaking.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)

    results = solr.get_number_random_records(core, 10)

    return render_template('theme.html', text=text, results=results, core=core)

# route for working theme page
@hidden.route('/hidden/working/')
def working():
    core = 'working'
    with open('content/hidden/working.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)

    results = solr.get_number_random_records(core, 10)

    return render_template('theme.html', text=text, results=results, core=core)

# route for resourceful theme page
@hidden.route('/hidden/resourceful/')
def resourceful():
    core = 'resourceful'
    with open('content/hidden/resourceful.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)

    results = solr.get_number_random_records(core, 10)

    return render_template('theme.html', text=text, results=results, core=core)
