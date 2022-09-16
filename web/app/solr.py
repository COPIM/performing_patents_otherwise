# @name: solr.py
# @creation_date: 2022-09-07
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <simon.bowie.19@gmail.com>
# @purpose: Performs Solr functions
# @acknowledgements:
# pycountry module for country data: https://pypi.org/project/pycountry/

import os
import requests
import re
import urllib
import random
import pycountry
from . import ops

# get config variables from OS environment variables: set in env file passed through Docker Compose
solr_hostname = os.environ.get('SOLR_HOSTNAME')
solr_port = os.environ.get('SOLR_PORT')

def solr_search(solrurl):
    # get result
    request = requests.get(solrurl)
    # turn the API response into useful Json
    json = request.json()

    num_found = json['response']['numFound']
    facets = []

    if (num_found == 0):
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
        try:
            json['facet_counts']
            facets = json['facet_counts']['facet_fields']
        except KeyError:
            pass

    return output, num_found, facets

def query_search(core, sort, query, country, year):

    # assemble parameters for the query string to Solr
    if (sort == 'relevance'):
        sort_parameter = ''
    else:
        sort_parameter = '&sort=' + sort

    if (query is None or query == 'None'):
        query_parameter = '&q=*%3A*'
    else:
        query_parameter = '&q=content%3A' + urllib.parse.quote_plus(query)

    if (country is None or country == 'None'):
        country_parameter = ''
    else:
        field = 'country'
        country_parameter = '&fq=%7B!term%20f%3D' + field + '%7D' + country

    if (year is None or year == 'None'):
        year_parameter = ''
    else:
        field = 'year'
        year_parameter = '&fq=%7B!term%20f%3D' + field + '%7D' + year

    # assemble a query string to send to Solr. This uses the Solr hostname from config.env. Solr's query syntax can be found at many sites including https://lucene.apache.org/solr/guide/6_6/the-standard-query-parser.html
    solrurl = 'http://' + solr_hostname + ':' + solr_port + '/solr/' + core + '/select?q.op=OR&indent=true' + query_parameter + '&wt=json' + sort_parameter + country_parameter + year_parameter + '&facet.field=country&facet.field=year&facet.sort=count&facet.mincount=1&facet=true'

    output = solr_search(solrurl)

    return output

def id_search(core, id):

    # assemble a query string to send to Solr. This uses the Solr hostname from config.env. Solr's query syntax can be found at many sites including https://lucene.apache.org/solr/guide/6_6/the-standard-query-parser.html
    solrurl = 'http://' + solr_hostname + ':' + solr_port + '/solr/' + core + '/select?q.op=OR&q=id%3A"' + id + '"&wt=json'

    output = solr_search(solrurl)

    return output

def random_search(core):

    rand = str(random.randint(0, 9999999))

    # assemble a query string to send to Solr. This uses the Solr hostname from config.env. Solr's query syntax can be found at many sites including https://lucene.apache.org/solr/guide/6_6/the-standard-query-parser.html
    solrurl = 'http://' + solr_hostname + ':' + solr_port + '/solr/' + core + '/select?q.op=OR&q=*%3A*&wt=json&sort=random_' + rand + '%20asc&rows=1'

    output = solr_search(solrurl)

    return output

def parse_result(id, input):

    output = {}

    output['id'] = id

    # set document reference number (used for OPS API)
    doc_ref = re.search('=D\s(([^\s]*)\s([^\s]*)\s([^\s]*))', input)
    if doc_ref is None:
        doc_ref = re.search('=D&locale=en_EP\s(([^\s]*)\s([^\s]*)\s([^\s]*))', input)
        if doc_ref is None:
            output['doc_ref'] = ""
        else:
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
    if ipc_publication is not None:
        if ipc_publication.group(1) is not None:
            output['ipc_publication_url'] = ipc_publication.group(1)

    # search for the title in the content element and display it
    title = re.search('Title.*?\\n(.*?)\\n|Tile.?\\n(.*?)\\n', input)
    if title is not None:
        if title.group(1) is not None:
            output['title'] = title.group(1)
        else:
            output['title'] = title.group(2)

    # search for the abstract in the content element and display it
    abstract = re.search('Abstract.*\n(.*)\n', input)
    if abstract is not None:
        if abstract.group(1) is not None:
            output['abstract'] = abstract.group(1)
    else:
        abstract = re.search('\(.*?\) (\\n\\n\\n\\n|\\n\\n\\n|\\n\\n)(.*)\\n', input)
        if abstract is not None:
            if abstract.group(2) is not None:
                output['abstract'] = abstract.group(2)

    # search for the year in the content element and display it
    year = re.search('=D[^\s]*\s[^\s]*\s[^\s]*\s[^\s]*\s(\d{4})', input)
    if year is not None:
        output['year'] = year.group(1)

    # search for the country in the content element and display it
    country_code = re.search('FT=D[^\s]*\s(\w{2})', input)
    if country_code is not None:
        country = pycountry.countries.get(alpha_2=country_code.group(1))
        if country is not None:
            output['country'] = country
        else:
            country = pycountry.historic_countries.get(alpha_2=country_code.group(1))
            if country is not None:
                output['country'] = country
            else:
                output['country'] = country_code.group(1)

    output['raw'] = input

    return output

def get_ten_random_elements(field):
    core = 'all'
    output = []
    i = 0
    while i <= 9:
        search_results = random_search(core)
        results = search_results[0]
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
        search_results = random_search(core)
        results = search_results[0]
        for result in results:
            if ops.get_images(result['doc_ref']):
                image = ops.get_images(result['doc_ref'])
                result.update(image)
                output.append(result)
                i += 1
    return output

def get_total_number(core):

    # Assemble a query string to send to Solr. This uses the Solr hostname from config.env. Solr's query syntax can be found at many sites including https://lucene.apache.org/solr/guide/6_6/the-standard-query-parser.html
    solrurl = 'http://' + solr_hostname + ':' + solr_port + '/solr/' + core + '/select?q.op=OR&q=*:*&wt=json'

    # get result
    request = requests.get(solrurl)
    # turn the API response into useful Json
    json = request.json()

    num_found = json['response']['numFound']

    return num_found

def get_term_data(field, core):

    # Assemble a query string to send to Solr. This uses the Solr hostname from config.env. Solr's query syntax can be found at many sites including https://lucene.apache.org/solr/guide/6_6/the-standard-query-parser.html
    solrurl = 'http://' + solr_hostname + ':' + solr_port + '/solr/' + core + '/terms?terms.fl=' + field + '&wt=json&terms.limit=1000&terms.sort=index'

    # get result
    request = requests.get(solrurl)
    # turn the API response into useful Json
    json = request.json()

    output = json['terms'][field]

    return output
