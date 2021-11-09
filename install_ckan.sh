#! /bin/bash

sudo apt update  
sudo apt install -y libpq5 redis-server nginx supervisor  
wget https://packaging.ckan.org/python-ckan_2.9-py3-focal_amd64.deb  
sudo dpkg -i python-ckan_2.9-py3-focal_amd64.deb  

# postgres
sudo -u postgres createuser -S -D -R -P ckan_user  
sudo -u postgres createdb -O ckan_user ckan_default -E utf-8  

# change password in ckan.ini

# Solr  
sudo apt install -y solr-tomcat  

# change port  
# From: <Connector port="8080" protocol="HTTP/1.1"
# To: <Connector port="8983" protocol="HTTP/1.1"
sudo vim /etc/tomcat9/server.xml

sudo mv /etc/solr/conf/schema.xml /etc/solr/conf/schema.xml.bak
sudo ln -s /usr/lib/ckan/default/src/ckan/ckan/config/solr/schema.xml /etc/solr/conf/schema.xml
sudo service tomcat9 restart


# Edit default config
sudo vim /etc/ckan/default/ckan.ini

# open all necessary ports
# use AWS security group subak-ckan

# create superuser
ckan -c /etc/ckan/default/ckan.ini sysadmin add laurence email=laurence@subak.org name=laurence

