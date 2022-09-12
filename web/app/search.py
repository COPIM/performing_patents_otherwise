# @name: search.py
# @creation_date: 2022-09-07
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: search route for search
# @acknowledgements:
# https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login

from flask import Blueprint, render_template, request
from . import solr
from . import ops

search = Blueprint('search', __name__)

# route for search page
@search.route('/search/', methods=['POST'])
def basic_search():
    search = request.form.get('search')
    if request.form.get('core') is not None:
        core = request.form.get('core')
    else:
        core = 'all'
    if request.form.get('sort') is not None:
        sort = request.form.get('sort')
    else:
        sort = 'relevance'
    results = solr.solr_search(core, sort, search)
    return render_template('search.html', results=results, search=search, core=core, sort=sort)

# route for id_search page
@search.route('/search/id/')
def id_search():
    if request.args.get('core') is not None:
        core = request.args.get('core')
    else:
        core = 'all'
    if request.args.get('sort') is not None:
        sort = request.args.get('sort')
    else:
        sort = 'relevance'
    id = request.args.get('id')
    results = solr.solr_search(core, sort, search, id)

    for result in results:
        publication_details = ops.get_publication_details(result['doc_ref'])
        result.update(publication_details)
        if ops.get_images(result['doc_ref']):
            image = ops.get_images(result['doc_ref'])
            result.update(image)

    return render_template('record.html', results=results)
