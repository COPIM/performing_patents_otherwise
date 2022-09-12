# @name: solr.py
# @version: 0.1
# @creation_date: 2022-09-07
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <simon.bowie.19@gmail.com>
# @purpose: Performs Solr functions
# @acknowledgements:

import os
import requests
import re
import urllib
import random
from . import ops

# get config variables from OS environment variables: set in env file passed through Docker Compose
solr_hostname = os.environ.get('SOLR_HOSTNAME')
solr_port = os.environ.get('SOLR_PORT')

def solr_search(core, sort, search=None, id=None):

    # Assemble a query string to send to Solr. This uses the Solr hostname from config.env. Solr's query syntax can be found at many sites including https://lucene.apache.org/solr/guide/6_6/the-standard-query-parser.html
    if id is not None:
        solrurl = 'http://' + solr_hostname + ':' + solr_port + '/solr/' + core + '/select?q.op=OR&q=id%3A"' + id + '"&wt=json'
    else:
        if (sort == 'relevance'):
            solrurl = 'http://' + solr_hostname + ':' + solr_port + '/solr/' + core + '/select?q.op=OR&q=content%3A' + urllib.parse.quote_plus(search) + '&wt=json'
        else:
            solrurl = 'http://' + solr_hostname + ':' + solr_port + '/solr/' + core + '/select?q.op=OR&q=content%3A' + urllib.parse.quote_plus(search) + '&wt=json&sort=' + sort

    # get result
    request = requests.get(solrurl)
    # turn the API response into useful Json
    json = request.json()

    if (json['response']['numFound'] == 0):
        output = 'no results found'
    else:
        output = []
        for result in json['response']['docs']:
            # set ID variable
            id = result['id']
            # set content variable
            content = result['content']
            # parse result
            result_output = parse_result(id, content)
            output.append(result_output)
    return output

def parse_result(id, input):

    output = {}

    output['id'] = id

    # set document reference number (used for OPS API)
    doc_ref = re.search('=D\s(([^\s]*)\s([^\s]*)\s([^\s]*))', input)
    if doc_ref is None:
        doc_ref = re.search('=D&locale=en_EP\s(([^\s]*)\s([^\s]*)\s([^\s]*))', input)
        output['doc_ref'] = doc_ref.group(1).replace(" ","")
    else:
        output['doc_ref'] = doc_ref.group(1).replace(" ","")

    # search for the application ID in the content element and display it
    application_id = re.search('Application.*\n(.*)\n', input)
    output['application_id'] = application_id.group(1)

    # search for the EPO publication URL in the content element and display it
    epo_publication = re.search('Publication.*\n(.*)\n', input)
    output['epo_publication_url'] = epo_publication.group(1)

    # search for the IPC publication URL in the content element and display it
    ipc_publication = re.search('IPC.*\n(.*)\n', input)
    output['ipc_publication_url'] = ipc_publication.group(1)

    # search for the title in the content element and display it
    title = re.search('Title.*\n(.*)\n', input)
    if title is not None:
        output['title'] = title.group(1)

    # search for the abstract in the content element and display it
    abstract = re.search('Abstract.*\n(.*)\n', input)
    if abstract is None:
        abstract = re.search('\(.\) \\n\\n(.*)\\n', input)
    if abstract is not None:
        output['abstract'] = abstract.group(1);

    # search for the year in the content element and display it
    year = re.search('=D[^\s]*\s[^\s]*\s[^\s]*\s[^\s]*\s(\d{4})', input)
    if year is not None:
        output['year'] = year.group(1)
    return output

def get_random_record(core):

    rand = str(random.randint(0, 9999999))

    # Assemble a query string to send to Solr. This uses the Solr hostname from config.env. Solr's query syntax can be found at many sites including https://lucene.apache.org/solr/guide/6_6/the-standard-query-parser.html
    solrurl = 'http://' + solr_hostname + ':' + solr_port + '/solr/' + core + '/select?q.op=OR&q=*%3A*&wt=json&sort=random_' + rand + '%20asc&rows=1'

    # get result
    request = requests.get(solrurl)
    # turn the API response into useful Json
    json = request.json()

    if (json['response']['numFound'] == 0):
        output = 'no results found'
    else:
        output = []
        for result in json['response']['docs']:
            # set ID variables
            id = result['id']
            # set content variable
            content = result['content']
            # parse result
            result_output = parse_result(id, content)
            output.append(result_output)
    return output

def get_ten_random_elements(field):
    core = 'all'
    output = []
    i = 0
    while i <= 9:
        results = get_random_record(core)
        for result in results:
            if field in result:
                dict = {'id': result['id'], field: result[field]}
                output.append(dict)
                i += 1
    return output

def get_ten_random_images():
    core = 'all'
    output = []
    i = 0
    while i <= 9:
        results = get_random_record(core)
        for result in results:
            if ops.get_images(result['doc_ref']):
                image = ops.get_images(result['doc_ref'])
                result.update(image)
                output.append(result)
                i += 1
    return output
