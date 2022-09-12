# @name: random.py
# @creation_date: 2022-09-09
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: random route for random
# @acknowledgements:

from flask import Blueprint, render_template, request
from . import solr
from . import ops

random = Blueprint('random', __name__)

# route for random page
@random.route('/random/')
def random_record():
    core = 'all'
    results = solr.get_random_record(core)
    for result in results:
        publication_details = ops.get_publication_details(result['doc_ref'])
        result.update(publication_details)
        if ops.get_images(result['doc_ref']):
            image = ops.get_images(result['doc_ref'])
            result.update(image)
    return render_template('record.html', results=results)

# route for comparing two random records
@random.route('/random/two/')
def two_random_records():
    core = 'all'
    results_list = []
    i = 0
    while i <= 1:
        results = solr.get_random_record(core)
        for result in results:
            publication_details = ops.get_publication_details(result['doc_ref'])
            result.update(publication_details)
            if ops.get_images(result['doc_ref']):
                image = ops.get_images(result['doc_ref'])
                result.update(image)
        results_list.append(result)
        i += 1
    return render_template('compare.html', results=results_list)

# route for getting ten random titles
@random.route('/random/titles/')
def ten_random_titles():
    titles = solr.get_ten_random_elements('title')
    additional_titles = solr.get_ten_random_elements('title')
    return render_template('titles.html', titles=titles, additional_titles=additional_titles)

# route for getting ten random abstracts
@random.route('/random/abstracts/')
def ten_random_abstracts():
    abstracts = solr.get_ten_random_elements('abstract')
    return render_template('abstracts.html', abstracts=abstracts)

# route for getting ten random images
@random.route('/random/images/')
def ten_random_images():
    results = solr.get_ten_random_images()
    return render_template('images.html', results=results)
