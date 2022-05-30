import json
import os

from dotenv import load_dotenv
import requests

load_dotenv()

N_DATASETS_PER_QUERY = 1000
API_KEY = os.getenv('API_KEY')
headers = {"Authorization": API_KEY}

# base_url = "https://data.subak.org"; verifySSL = True
base_url = "https://localhost"; verifySSL = False

with open('countries-iso-3166.json') as f:
    countries = json.load(f)

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

n_updated = 0
for ds in datasets:
    name = ds['name']
    
    # Skip datasets where geo region is already set or no countries are set
    if ('subak_geo_region' in ds.keys() and len(ds['subak_geo_region']) > 0) or 'subak_countries' not in ds.keys() or len(ds['subak_countries']) == 0:
        continue
    
    # Find region from listed countries
    regions = list(set([c['region'] for c in countries for dc in ds['subak_countries'] if c['alpha-2'] == dc]))
    
    # Set region to world if more than one region found
    region = regions[0].lower() if len(regions) == 1 else 'world'
    # print(name, region)
    
    # Update dataset with found countries
    data = {
        'id': name,
        'subak_geo_region': region
    }
    url = f'{base_url}/api/3/action/package_patch'
    print(url, data)
    r = requests.post(url, headers=headers, json=data, verify=verifySSL)
    if r.status_code == 200:
        print(f"Successfully updated region for dataset {name} with {region}")
        n_updated += 1
    else:
        print(f"Failed to update dataset {name} - {r.json()['error']}")
    
print(f"Updated regions for {n_updated}/{len(datasets)} datasets")