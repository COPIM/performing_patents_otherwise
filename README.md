# Archival Conversations patents data search engine

This repository contains the Docker Compose, Nginx, Python, and Solr config files for deploying the development environment for the Archival Conversations patents data search engine site.

## to deploy environment

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

## populating Apache Solr

In order to fill the site with documents, you will have to populate the Apache Solr search engine. There is a solr_import.sh script to help with this. Place whatever files you want indexed in a directory called 'data' within the main directory.

In solr_import.sh, change the directory to point to the main directory and, if necessary, change the location parameters for the various cores.

We use different Solr cores for the different themes on the site: 'all' is a core containing all documents while 'active', 'expanding', etc. contain only documents for that theme.

### legacy Solr commands

This section should be fully superseded by solr_import.sh and including the Solr config in the repository. These are left here for reference.

Created core using:

`docker exec -it solr solr create_core -c epo_data`

Note this fix to ensure that .rtf files can be indexed using Apache Tika: https://gitmemory.com/issue/docker-solr/docker-solr/341/682877640. Once you've created the core, run these commands:

`docker exec -ti --user=solr solr bash -c 'cp -r /opt/solr/example/files/conf/* /var/solr/data/{CORE_NAME}/conf/'`

`docker restart solr`

Add files to Solr using:

`docker run --rm -v "/Users/ad7588/Downloads/2018 (10381):/2018" --network=host solr:latest post -c epo_data /2018`
