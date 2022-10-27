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

    core = 'active'
    results_list = []
    i = 0
    while i <= 9:
        search_results = solr.random_search(core)
        results = search_results[0]
        for result in results:
            results_list.append(result)
        i += 1

    return render_template('theme.html', text=text, results=results_list)
