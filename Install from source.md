## Connect to instance
ssh -i ~/.ssh/ckan.pem ubuntu@52.56.165.207

## Create EC2 instance

## Install CKAN
Install CKAN from package  
https://docs.ckan.org/en/2.9/maintaining/installing/install-from-package.html  

sudo apt update  
sudo apt install -y libpq5 redis-server nginx supervisor  
wget https://packaging.ckan.org/python-ckan_2.9-py3-focal_amd64.deb  
sudo dpkg -i python-ckan_2.9-py3-focal_amd64.deb  

create postgres user  
sudo -u postgres createuser -S -D -R -P ckan_user  

sudo -u postgres createdb -O ckan_user ckan_default -E utf-8  

Solr  
sudo apt install -y solr-tomcat  

# change port  
sudo vim /etc/tomcat9/server.xml

sudo mv /etc/solr/conf/schema.xml /etc/solr/conf/schema.xml.bak
sudo ln -s /usr/lib/ckan/default/src/ckan/ckan/config/solr/schema.xml /etc/solr/conf/schema.xml


# filestore
# check the docs
