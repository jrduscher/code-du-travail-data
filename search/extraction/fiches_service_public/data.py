import argparse
import json
import logging
import os

from pprint import pformat

from search import settings


logger = settings.get_logger(__name__)


JSON_FICHES = os.path.join(settings.BASE_DIR, 'dataset/fiches-sp-travail.json')

FICHES_SERVICE_PUBLIC = []

def populate_fiches_service_public(json_file=JSON_FICHES):

    with open(json_file) as json_data:

        data = json.load(json_data)

        TAGS_IRRELEVANT = ['Accueil particuliers', 'Travail']

        for item in data:

            text = item.get('intro', '') + item.get('text', '') + item.get('situations', '')
            if not text:
                logger.debug('No text found for title: %s\n%s', item['title'], item['url'])

            # Replace new lines by spaces.
            text = ' '.join(text.split('\n'))
            # Replace multiple spaces by a single space.
            text = ' '.join(text.split())

            # Merge all tags.
            tags = list(set(
                item['tags']
                + [item for item in item['ariane'] if item not in TAGS_IRRELEVANT]
                + item['fiches']
                + item['sousDossiers']
            ))

            fiche = {
                'url': item['url'],
                'sous_theme': item['sousTheme'],
                'title': item['title'],
                'text': text,
                'tags': tags,
                'refs': item['refs'],  # List of {`url`, `source` and `sujet`} entries.
            }
            FICHES_SERVICE_PUBLIC.append(fiche)

            logger.debug('-' * 80)
            logger.debug(pformat(fiche))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    populate_fiches_service_public()

else:

    populate_fiches_service_public()