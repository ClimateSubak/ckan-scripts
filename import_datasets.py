import os
import pprint

import requests
from dotenv import load_dotenv

load_dotenv()

# Dataset details
# Organisations must be already created
dataset_dict = {
    'name': 'my_dataset_name',
    'notes': 'A long description of my dataset',
    'owner_org': 'subak'
}

#url = 'http://data.climatesubak.org/api/action/package_create'

url = 'http://docker.for.mac.localhost:5000/api/action/package_create'

headers = {'Authorization': os.getenv('API_KEY')}

# Make the HTTP request.
response = requests.post(url, data=dataset_dict, headers=headers)
assert response.status_code == 200

# Get response
response_dict = response.json()
assert response_dict['success'] is True

# package_create returns the created package as its result.
created_package = response_dict['result']
pprint.pprint(created_package)
