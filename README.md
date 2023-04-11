# Performing Patents Otherwise patents data search engine

This repository contains the Docker Compose, Nginx, Python, and Solr config files for deploying the development and production environments for the Performing Patents Otherwise publication comprising a search engine, archive interventions, and Markdown text for chapters.

## application structure

The Performing Patents Otherwise publication is a Python application using the [Flask](https://flask.palletsprojects.com/en/2.2.x/) framework to render as a website and to provide functions around querying the Solr index and fetching data from the European Patent Office's Open Patent Services API. The Flask framework uses a few HTML template pages to render different pages efficiently based on routes defined in Python files.

The application is then made available through the [Gunicorn](https://gunicorn.org/) WSGI HTTP Server and served to the web by [Nginx](https://nginx.org/). 

![diagram of the application architecture](https://github.com/COPIM/politics_of_patents/blob/main/web/app/static/images/patents_site_architecture.png?raw=true)

The search engine is an [Apache Solr](https://solr.apache.org/) 8.11.1 search engine. Solr is a reliable open source search engine that provides full-text search, faceted search, and advanced customisation. Solr is able to index RTF files using [Apache Tika’s](https://tika.apache.org/) framework for extracting metadata and text from a range of document formats. Solr indexes all the patent documents and then presents that index via an API for querying. This is available on port 8983 when running locally. Some Solr config is kept in ./solr_config to perform custom indexing for year and country data.

The application queries the European Patent Office's [Open Patent Services API](https://www.epo.org/searching-for-patents/data/web-services/ops.html) to pull in extra data for each patent such as original language title, original language abstract, and images of the original patents.

> "Open Patent Services (OPS) is a web service which provides access to the EPO's raw data via a standardised XML interface. It does this using RESTful architecture. OPS data is extracted from the EPO's bibliographic, worldwide legal status, full-text and image databases. It is therefore from the same sources as the Espacenet and European Patent Register data." 

The OPS API connection is set up in config.env using the hostname https://ops.epo.org/ for patent data, http://ops.epo.org/ for image data, and API credentials registered at https://developers.epo.org/. The terms of use for this API are available at [https://www.epo.org/footer/terms.html](https://www.epo.org/footer/terms.html).

## deploying the environment

### config.env

To deploy this environment, first copy config.env.template to a new file, config.env. Fill in the appropriate environment variables.

Note that on Mac the Python container has to communicate with the Solr container using the hostname 'host.docker.internal' rather than 'localhost' or '127.0.0.1': https://stackoverflow.com/questions/24319662/from-inside-of-a-docker-container-how-do-i-connect-to-the-localhost-of-the-mach

On Linux, you can use the container name e.g. 'solr' as the Solr hostname in config.env.

### Docker Compose

In the command line, navigate to the directory where this repository is stored on your local machine and run:

`docker-compose up -d --build`

Docker should build the application environment comprising a Python container (including ImageMagick), an Apache Solr container (deployed Solr for .rtf indexing using instructions at: https://github.com/docker-solr/docker-solr), and an Nginx web server to serve the website.

The website should then be available in the browser at 'localhost:5000'.

To take down the environment, run:

`docker-compose down`

### populating the index

In order to fill the site with documents, you will have to populate the Apache Solr search engine. There is a solr_import.sh script to help with this. Place whatever files you want indexed in a directory called 'data' within the main directory.

In solr_import.sh, change the directory to point to the main directory and, if necessary, change the location parameters for the various cores.

We use different Solr cores for the different themes on the site: 'all' is a core containing all documents while 'active', 'expanding', etc. contain only documents for that theme.

#### legacy Solr commands

This section should be fully superseded by solr_import.sh and including the Solr config in the repository. These are left here for reference.

Created core using:

`docker exec -it solr solr create_core -c epo_data`

Note this fix to ensure that .rtf files can be indexed using Apache Tika: https://gitmemory.com/issue/docker-solr/docker-solr/341/682877640. Once you've created the core, run these commands:

`docker exec -ti --user=solr solr bash -c 'cp -r /opt/solr/example/files/conf/* /var/solr/data/{CORE_NAME}/conf/'`

`docker restart solr`

Add files to Solr using:

`docker run --rm -v "/Users/ad7588/Downloads/2018 (10381):/2018" --network=host solr:latest post -c epo_data /2018`
