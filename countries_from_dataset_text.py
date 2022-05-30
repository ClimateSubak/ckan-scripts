import json
import os
import re

from dotenv import load_dotenv
import pandas as pd
import requests

load_dotenv()

N_DATASETS_PER_QUERY = 1000
API_KEY = os.getenv('API_KEY')
headers = {"Authorization": API_KEY}

# base_url = "https://data.subak.org"; verifySSL = True
base_url = "https://localhost"; verifySSL = False

with open('countries-iso-3166.json') as f:
    countries = json.load(f)
country_names = [c['name'] for c in countries]

datasets = []
more_datasets = True
n = 0

# Recursively get all datasets
print('Gathering datasets...')
while more_datasets:
    r = requests.get(f'{base_url}/api/3/action/current_package_list_with_resources?limit={N_DATASETS_PER_QUERY}&offset={n*N_DATASETS_PER_QUERY}', verify=verifySSL)
    if r.status_code != 200:
        print(r.status_code, r.text)
        raise requests.HTTPError
    
    _datasets = r.json()['result']
    
    if len(_datasets) > 0:
        datasets = datasets + _datasets 
        n += 1
    else:
        more_datasets = False

n_not_found = 0
for ds in datasets:
    name = ds['name']
    # Skip datasets where countries are already set
    if 'subak_countries' in ds.keys() and len(ds['subak_countries']) > 0:
        continue
    
    # Ignore metadata that might wrongly indicate that the dataset is about a certain country
    ignore_keys = ['organization']
    for key in ignore_keys:
        ds.pop(key, None)
        
    # Flatten metadata values to a single string and search for country names
    flat_ds_values = list(pd.json_normalize(ds).to_dict(orient='records')[0].values())
    text_blob = ' '.join([str(v) for v in flat_ds_values])    
    found_countries = [c for c in country_names if re.search(fr'\W{c.lower()}\W', text_blob.lower()) is not None]
    # print(name, found_countries)
    
    # Skip datasets where we can't find any country names in the metadata
    if len(found_countries) == 0:
        n_not_found += 1
        continue
    
    # Convert country_names to country codes
    country_codes = [c['alpha-2'] for c in countries for fc in found_countries if c['name'] == fc]
    
    # Update dataset with found countries
    data = {
        'id': name,
        'subak_countries': country_codes
    }
    url = f'{base_url}/api/3/action/package_patch'
    # print(url, data)
    r = requests.post(url, headers=headers, json=data, verify=verifySSL)
    if r.status_code == 200:
        print(f"Successfully updated countries on dataset {name} with {country_codes}")
    else:
        print(f"Failed to update dataset {name} - {r.json()['error']}")
    
print(f"Could not determine countries for {n_not_found}/{len(datasets)} datasets")