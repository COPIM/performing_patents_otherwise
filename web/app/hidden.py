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
    with open('content/section_3/intro-hidden.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)
    return render_template('text.html', text=text)

# route for expanding theme page
@hidden.route('/hidden/expanding/')
def expanding():
    core = 'expanding'
    with open('content/section_3/expanding.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)

    results = solr.get_number_random_records(core, 10)

    return render_template('theme.html', text=text, results=results, core=core)

# route for active theme page
@hidden.route('/hidden/active/')
def active():
    core = 'active'
    with open('content/section_3/active.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)

    results = solr.get_number_random_records(core, 10)

    return render_template('theme.html', text=text, results=results, core=core)

# route for secret theme page
@hidden.route('/hidden/secret/')
def secret():
    core = 'secret'
    with open('content/section_3/secret.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)

    results = solr.get_number_random_records(core, 10)

    return render_template('theme.html', text=text, results=results, core=core)

# route for leaking theme page
@hidden.route('/hidden/leaking/')
def leaking():
    core = 'leaking'
    with open('content/section_3/leaking.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)

    results = solr.get_number_random_records(core, 10)

    return render_template('theme.html', text=text, results=results, core=core)

# route for working theme page
@hidden.route('/hidden/working/')
def working():
    core = 'working'
    with open('content/section_3/working.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)

    results = solr.get_number_random_records(core, 10)

    return render_template('theme.html', text=text, results=results, core=core)

# route for resourceful theme page
@hidden.route('/hidden/resourceful/')
def resourceful():
    core = 'resourceful'
    with open('content/section_3/resourceful.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)

    results = solr.get_number_random_records(core, 10)

    return render_template('theme.html', text=text, results=results, core=core)
