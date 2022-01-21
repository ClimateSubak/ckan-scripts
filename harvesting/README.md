# CKAN harvester

This file documents how to harvest datasets from other CKAN instances. It is intended that the Climate Subak data catalogue contains datasets from a wide variety of sources.

## Start the necessary queues for harvester
`docker-compose -f docker-compose.<env>.yml exec ckan /bin/bash -c "ckan harvester gather_consumer"`\
`docker-compose -f docker-compose.<env>.yml exec ckan /bin/bash -c "ckan harvester fetch_consumer"`

## Create a harvest job in the web UI
- Navigate to `http://<ckan-url>/harvest/new`
- Enter the URL of the CKAN instance you want to harvest
- Enter a unique title for the harvest source
- Select `CKAN` as the source type
- Select the frequency to harvest from the source
- In the configuration field enter the following in order to harvest the orgs as well as datasets from the harvest source (or omit to assign datasets to a default org: `{"remote_orgs": "create"}`. Other config options are detailed [here](https://github.com/ckan/ckanext-harvest/#the-ckan-harvester)
- Select the default org to assign datasets to (required even if you are harvesting the orgs from the source))

To start harvest jobs, run: `docker-compose -f docker-compose.<env>.yml exec ckan-dev /bin/bash -c "ckan harvester run"`

Jobs will not show a finished status until the command above is run again.
