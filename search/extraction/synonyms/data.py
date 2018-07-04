import argparse
import json
import logging
import os

from pprint import pformat

from search import settings


logger = settings.get_logger(__name__)


SYNONYMS = []

# TESS.json => Thesaurus Travail Emploi Santé Solidarité.
JSON_FILE = os.path.join(settings.BASE_DIR, 'dataset/thesaurus/TESS.json')


def populate_synonyms(json_file=JSON_FILE):
    """
    Extract synonyms from the TESS Thesaurus.
    """

    with open(json_file) as json_data:

        data = json.load(json_data)

        for item in data:

            if item.get('term') and item.get('equivalent'):
                SYNONYMS.append(f"{item['term']}, {item['equivalent']}")


        logger.debug('-' * 80)
        logger.debug(pformat(SYNONYMS, width=120))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    populate_synonyms()

else:

    populate_synonyms()
