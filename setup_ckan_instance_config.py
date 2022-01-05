import os

import requests
from dotenv import load_dotenv

load_dotenv()

# CKAN config items to update
config_options = {
    'ckan.site_title': 'Subak Data Catalogue',
    'ckan.site_description': 'Share the data, save the planet',
    'ckan.site_logo': 'https://images.squarespace-cdn.com/content/v1/5fbe3c75a5bc066edf9513f2/1606745984909-KHIUHFOBXP5NTTNVMG5B/SUBAK_LOGO.png'
}

# Get about text
response = requests.get('https://raw.githubusercontent.com/ClimateSubak/docker-ckan/main/ABOUT.md')
assert response.status_code == 200
content = response.text
config_options['ckan.site_about'] = content

#url = 'http://data.climatesubak.org/api/action/config_option_update'
url = 'http://localhost:5000/api/action/config_option_update'

headers = {'Authorization': os.getenv('API_KEY')}

# Make the HTTP request.
response = requests.post(url, data=config_options, headers=headers)
assert response.status_code == 200

# Get response
response_dict = response.json()
assert response_dict['success'] is True

# package_create returns the created package as its result.
res = response_dict['result']
print(res)
