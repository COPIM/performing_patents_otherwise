# @name: ops.py
# @version: 0.1
# @creation_date: 2022-09-08
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <simon.bowie.19@gmail.com>
# @purpose: Performs functions against the European Patent Office's Open Patent Services (OPS) API
# @acknowledgements:
# OPS documented at https://www.epo.org/searching-for-patents/data/web-services/ops.html
# OPS RESTful API specification at http://documents.epo.org/projects/babylon/eponet.nsf/0/F3ECDCC915C9BCD8C1258060003AA712/$File/ops_v3.2_documentation_-_version_1.3.18_en.pdf
# OPS API functions list at https://developers.epo.org/ops-v3-2/apis

import os
import requests
import base64
from wand.image import Image

# get config variables from OS environment variables: set in env file passed through Docker Compose
ops_url = os.environ.get('OPS_URL')
ops_url_images = os.environ.get('OPS_URL_IMAGES')
consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')

def get_access_token():

    # OPS API credentials (details at http://documents.epo.org/projects/babylon/eponet.nsf/0/F3ECDCC915C9BCD8C1258060003AA712/$File/ops_v3.2_documentation_-_version_1.3.18_en.pdf)
    endpoint_url = ops_url + '3.2/auth/accesstoken'
    auth = consumer_key + ":" + consumer_secret
    auth_bytes = auth.encode("ascii")
    base64_bytes = base64.b64encode(auth_bytes)
    base64_string = base64_bytes.decode("ascii")

    # set up API call
    headers = {"Authorization": "Basic " + base64_string, "Content-Type": "application/x-www-form-urlencoded"}
    data = "grant_type=client_credentials"

    # give back result
    response = requests.post(endpoint_url, headers=headers, data=data)

    if response.status_code == 200:
        # turn the API response into useful Json
        json = response.json()
        access_token = json['access_token']

    return access_token

def get_publication_details(doc_ref):

    access_token = get_access_token()

    # OPS API credentials (details at http://documents.epo.org/projects/babylon/eponet.nsf/0/F3ECDCC915C9BCD8C1258060003AA712/$File/ops_v3.2_documentation_-_version_1.3.16_en.pdf)
    endpoint_url = ops_url + 'rest-services/published-data/publication/docdb/' + doc_ref + '/biblio'

    # set up API call
    headers = {"Authorization": "Bearer " + access_token, "Accept": "application/json"}

    # get result
    response = requests.get(endpoint_url, headers=headers)

    output = {}

    if response.status_code == 200:
        # turn the API response into useful Json
        json = response.json()

        # for each invention title, check if it's in the original language
        try:
            json['ops:world-patent-data']['exchange-documents']['exchange-document']['bibliographic-data']['invention-title']
            invention_titles = json['ops:world-patent-data']['exchange-documents']['exchange-document']['bibliographic-data']['invention-title']
            try:
                invention_titles[1]
                for invention_title in invention_titles:
                    if invention_title['@lang'] is not None and invention_title['@lang'] != 'en':
                        output['original_title'] = invention_title['$']
            except KeyError:
                if invention_titles['@lang'] is not None and invention_titles['@lang'] != 'en':
                    output['original_title'] = invention_titles['$']
        except KeyError:
            pass

        # for each abstract, check if it's in the original language
        try:
            json['ops:world-patent-data']['exchange-documents']['exchange-document']['abstract']
            abstracts = json['ops:world-patent-data']['exchange-documents']['exchange-document']['abstract']
            try:
                abstracts[1]
                for abstract in abstracts:
                    if abstract['@lang'] is not None and abstract['@lang'] != 'en':
                        output['original_abstract'] = abstract['p']['$']
            except KeyError:
                if abstracts['@lang'] is not None and abstracts['@lang'] != 'en':
                    output['original_abstract'] = abstracts['p']['$']
        except KeyError:
            pass

    return output

def get_images(doc_ref):

    access_token = get_access_token()

    # OPS API credentials (details at http://documents.epo.org/projects/babylon/eponet.nsf/0/F3ECDCC915C9BCD8C1258060003AA712/$File/ops_v3.2_documentation_-_version_1.3.16_en.pdf)
    endpoint_url = ops_url + 'rest-services/published-data/publication/docdb/' + doc_ref + '/images'

    # set up API call
    headers = {"Authorization": "Bearer " + access_token, "Accept": "application/json"}

    # give back result
    response = requests.get(endpoint_url, headers=headers)

    if response.status_code == 200:

        output = {}
        drawings_url = {}

        # turn the API response into useful Json
        json = response.json()

        try:
            json['ops:world-patent-data']['ops:document-inquiry']['ops:inquiry-result']['ops:document-instance']
            document_instances = json['ops:world-patent-data']['ops:document-inquiry']['ops:inquiry-result']['ops:document-instance']
            try:
                document_instances[0]
                for document_instance in document_instances:
                    if document_instance['@desc'] == 'Drawing':
                        drawings_url = ops_url_images + '3.2/rest-services/' +  document_instance['@link'] + '?Range=1'
                if drawings_url is None:
                    for document_instance in document_instances:
                        if document_instance['@desc'] == 'FullDocument':
                            drawings_url = ops_url_images + '3.2/rest-services/' +  document_instance['@link'] + '?Range=1'
            except KeyError:
                pass

            try:
                drawings_url[0]

                # set up API call
                headers = {"Authorization": "Bearer " + access_token, "Accept": "application/tiff"}

                # give back result
                response = requests.get(drawings_url, headers=headers)

                if response.status_code == 200:
                    with Image(blob = response.content) as image:
                        png_blob = image.make_blob('png')
                        base64_bytes = base64.b64encode(png_blob)
                        output['image'] = base64_bytes.decode("ascii")

            except KeyError:
                pass

        except KeyError:
            pass

    else:
        output = False

    return output
