import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')
headers = {"Authorization": API_KEY}

# TESTING

# Fetch tags
# curl https://data.climatesubak.org/api/3/action/tag_list | jq '.result' > tags.json

# data = {
#     'id': 'electric-car-count-uk-car-market-share-by-fuel-type',
#     'tags': [{'name': 'cars'}, {'name': 'new'}]
#     }

# Change tags
# headers={"Authorization": "XXX"}
# r = requests.post("https://data.climatesubak.org/api/3/action/package_patch", headers=headers, json=data)
# r.json()

base_url = "https://data.climatesubak.org"
verify = True
# base_url = "https://localhost"
# verify = False

r = requests.get(f'{base_url}/api/3/action/tag_list', verify=verify)
assert r.status_code == 200, "Tag list query failed"

# all fields - json with id
# {base_url}/api/3/action/tag_list?all_fields=True

tags = r.json()['result']

tags_to_clean = []

for tag in tags:
    if any(char.isupper() for char in tag) or '_' in tag or '-' in tag:
        tags_to_clean.append(tag)
assert len(tags_to_clean) > 0, "There are no tags to clean"
print(f'There are {len(tags_to_clean)} tags that need cleaning')

# get datasets for each tag
for tag in tags_to_clean:
    r = requests.get(f'{base_url}/api/3/action/package_search?fq=tags:{tag}', verify=verify)
    assert r.status_code == 200, f"Dataset search by tag failed for tag: {tag}"
    result = r.json()['result']

    # patch each dataset with cleaned tags
    for dataset in result['results']:
        name = dataset['name']
        tags = dataset['tags']
        new_tags = []
        for tag in tags:
            # just take the name from the tag dictionary
            new_tag = tag['name'].lower().replace('-', ' ').replace('_', ' ')
            new_tags.append({"name": new_tag})
        
        data = {
            'id': name,
            # new_tags should look like this [{'name': 'old_tag'}, {'name': 'new_tag'}]
            'tags': new_tags
        }
        url = f'{base_url}/api/3/action/package_patch'

        r = requests.post(url, headers=headers, json=data, verify=verify)
        try:
            assert r.status_code == 200
            print(f"Successfully cleaned tags on dataset {name}")
        except:
            print(f"Failed to update dataset {name} - {r.json['error']}")

