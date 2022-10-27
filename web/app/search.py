# @name: search.py
# @creation_date: 2022-09-07
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: search route for Section 1: Searching the archive
# @acknowledgements:
# https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login

from flask import Blueprint, render_template, request, redirect, url_for
from . import solr
from . import ops
import pycountry

search = Blueprint('search', __name__)

# route for basic search page
@search.route('/search/', methods=['GET', 'POST'])
def basic_search():
    if request.method == 'POST':
        if request.form.get('query') is not None:
            query = request.form.get('query')
        else:
            query = None
        if request.form.get('core') is not None:
            core = request.form.get('core')
        else:
            core = 'all'
        if request.form.get('sort') is not None:
            sort = request.form.get('sort')
        else:
            sort = 'relevance'
        if request.form.get('country') is not None:
            country = request.form.get('country')
        else:
            country = None
        if request.form.get('year') is not None:
            year = request.form.get('year')
        else:
            year = None
    else:
        if request.args.get('query') is not None:
            query = request.args.get('query')
        else:
            query = None
        if request.args.get('core') is not None:
            core = request.args.get('core')
        else:
            core = 'all'
        if request.args.get('sort') is not None:
            sort = request.args.get('sort')
        else:
            sort = 'relevance'
        if request.args.get('country') is not None:
            country = request.args.get('country')
        else:
            country = None
        if request.args.get('year') is not None:
            year = request.args.get('year')
        else:
            year = None
    if (query is None and country is None and year is None):
        return redirect(url_for('main.index'))
    else:
        search_results = solr.query_search(core, sort, query, country, year)
        results = search_results[0]
        num_found = search_results[1]
        year_facet = search_results[2]['year']
        country_facet = search_results[2]['country']
        for i in range(0, len(country_facet)):
            if i % 2 == 0:
                country_full = pycountry.countries.get(alpha_2=country_facet[i])
                if country_full is not None:
                    country_facet[i] = country_full
                else:
                    country_full = pycountry.historic_countries.get(alpha_2=country_facet[i])
                    if country_full is not None:
                        country_facet[i] = country_full
        total_number = solr.get_total_number(core)
        return render_template('search.html', results=results, num_found=num_found, total_number=total_number, country_facet=country_facet, year_facet=year_facet, query=query, core=core, sort=sort, country=country, year=year)

# route for id_search page
@search.route('/search/id/', methods=['GET'])
def id_search():
    if request.args.get('id') is None:
        return redirect(url_for('main.index'))
    else:
        id = request.args.get('id')
    if request.args.get('core') is not None:
        core = request.args.get('core')
    else:
        core = 'all'
    search_results = solr.id_search(core, id)
    results = search_results[0]
    for result in results:
        publication_details = ops.get_publication_details(result['doc_ref'])
        result.update(publication_details)
        if ops.get_images(result['doc_ref']):
            image = ops.get_images(result['doc_ref'])
            result.update(image)

    return render_template('record.html', results=results)
