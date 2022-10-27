# @name: interventions.py
# @creation_date: 2022-09-09
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: inteventions route for Section 2: Search Interventions
# @acknowledgements:

from flask import Blueprint, render_template, request
from . import solr
from . import ops

interventions = Blueprint('interventions', __name__)

# route for random entry page ('A random entry')
@interventions.route('/interventions/random/')
def random_record():
    core = 'all'
    search_results = solr.random_search(core)
    results = search_results[0]
    for result in results:
        publication_details = ops.get_publication_details(result['doc_ref'])
        result.update(publication_details)
        if ops.get_images(result['doc_ref']):
            image = ops.get_images(result['doc_ref'])
            result.update(image)
    return render_template('record.html', results=results)

# route for comparing two random records ('A juxtaposition of two')
@interventions.route('/interventions/juxtaposition/')
def two_random_records():
    core = 'all'
    results_list = []
    i = 0
    while i <= 1:
        search_results = solr.random_search(core)
        results = search_results[0]
        for result in results:
            publication_details = ops.get_publication_details(result['doc_ref'])
            result.update(publication_details)
            if ops.get_images(result['doc_ref']):
                image = ops.get_images(result['doc_ref'])
                result.update(image)
        results_list.append(result)
        i += 1
    return render_template('compare.html', results=results_list)

# route for getting ten random titles ('A poetics of titles')
@interventions.route('/interventions/titles/')
def ten_random_titles():
    titles = solr.get_ten_random_elements('title')
    additional_titles = solr.get_ten_random_elements('title')
    return render_template('titles.html', titles=titles, additional_titles=additional_titles)

# route for getting ten random abstracts ('A handful of fragments')
@interventions.route('/interventions/fragments/')
def ten_random_abstracts():
    abstracts = solr.get_ten_random_elements('abstract')
    return render_template('abstracts.html', abstracts=abstracts)

# route for getting ten random images ('A scattering of images')
@interventions.route('/interventions/scattering/')
def random_images():
    images = solr.get_random_images(4)
    additional_images = solr.get_random_images(6)
    return render_template('images.html', images=images, additional_images=additional_images)
