Change platform to arm/x86 in docker-compose

Use docker exec to make changes: 
docker exec -it ckan /usr/local/bin/ckan -c /etc/ckan/production.ini sysadmin add laurence
