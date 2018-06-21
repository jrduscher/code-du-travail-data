import json
import os

from indexation.settings import BASE_DIR

JSON_FICHES = os.path.join(BASE_DIR, 'dataset/fiches-sp-travail.json')

FICHES_SERVICE_PUBLIC = []

def inspect_dict(json_file=JSON_FICHES):

    with open(json_file) as json_data:
        data = json.load(json_data)
        for item in data:
            FICHES_SERVICE_PUBLIC.append({
                'title': item['title'],
                'url': item['url'],
                'tags': item['tags'],
                # Textes de référence: "sujets".
                'refs_sujets': [ref['sujet'] for ref in item['refs'] if ref.get('sujet')],
                # Textes de référence: "sources".
                'refs_sources': [ref['source'] for ref in item['refs']],
            })

inspect_dict()
