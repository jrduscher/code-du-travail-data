import argparse
import json
import logging
import os

from pprint import pformat

from search import settings


logger = settings.get_logger(__name__)


JSON_FICHES = os.path.join(settings.BASE_DIR, 'dataset/fiches_ministere_travail/fiches-min-travail.json')

FICHES_MINISTERE_TRAVAIL = []

def populate_fiches_ministere_travail(json_file=JSON_FICHES):

    with open(json_file) as json_data:

        data = json.load(json_data)

        for item in data:

            text = item['text']
            text = text.replace('A SAVOIR', '')
            text = ' '.join(text.split())  # Replace multiple spaces by a single space.

            fiche = {
                'title': item['title'],
                'text': text,
                'questions': item['summary'],  # Summary = questions.
                'url': item['url'],
            }

            FICHES_MINISTERE_TRAVAIL.append(fiche)

            logger.debug('-' * 80)
            logger.debug(pformat(fiche))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    populate_fiches_ministere_travail()

else:

    populate_fiches_ministere_travail()
