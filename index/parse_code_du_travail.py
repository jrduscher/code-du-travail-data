"""
Merge the Legilibre's `Code du travail` source and the ePoseidon classification.
"""
import argparse
import json
import logging
import os
import re

from collections import defaultdict, namedtuple


logging.basicConfig(level=logging.WARNING, format='%(funcName)s() %(message)s')


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


STATS = {
    'count_article': 0,
    'eposeidon_sources': defaultdict(int),
    'eposeidon_tags': defaultdict(int),
}


# A global dict that will be used to populate Elasticsearch.
CODE_DU_TRAVAIL_DICT = {}


# A global dict where each key is the number of a `Code du travail`'s
# article and each value is a set of one or more ePoseidon's tag.
# Python's sets are used to avoid duplicates:
# {
#     'R742-9': {
#         EposeidonTag(
#             source='Code du travail',
#             tags='Négociations collectives > Négo collective, Accords > Maritime > Maritime',
#             tags_levels=4
#         ),
#     },
#     ...
# }
EPOSEIDON_TAGS_DICT = defaultdict(set)
EposeidonTag = namedtuple('EposeidonTag', ['source', 'tags', 'tags_levels'])


def populate_eposeidon_tags_dict(
    json_file=os.path.join(BASE_DIR, 'dataset/codification-articles-eposeidon-20180404.json')):
    """
    Populate `EPOSEIDON_TAGS_DICT` with "tags" extracted from the existing
    ePoseidon's codification of the `Code du travail`.
    """

    with open(json_file) as json_data:

        data = json.load(json_data)

        # Each key is a reference to an article.
        # An article can be related to multiple sources, e.g. article "1" can be:
        # - article 1 of "Décret n°2005-305 du 31 mars 2005"
        # - article 1 of "Règlement 561-2006 du 15 mars 2006 Transport routier Durée du travail"
        # etc.
        for article_num in data:

            for article in data[article_num]:

                source = article['attrs']['source']

                if not source:
                    logging.debug('Skipping item in article "%s" because its `source` was empty.', article_num)
                    continue

                multiple_spaces = r'\s+'
                single_space = ' '
                # TODO: fix typos in tags, replace abbreviations etc.
                tags = [
                    # Level 1 = Theme.
                    re.sub(multiple_spaces, single_space, article['Theme']['nom']).strip(),
                    # Level 2 = SousTheme.
                    re.sub(multiple_spaces, single_space, article['SousTheme']['nom']).strip(),
                    # Level 3 = Objet.
                    re.sub(multiple_spaces, single_space, article['Objet']['nom']).strip(),
                    # Level 4 = Aspect (may not exist in the source file).
                    re.sub(multiple_spaces, single_space, article.get('Aspect', {}).get('nom', '')).strip(),
                ]
                tags_str = (' > ').join(tag for tag in tags if tag)

                tags_levels = len([tag for tag in tags if tag])

                EPOSEIDON_TAGS_DICT[article_num].add(
                    EposeidonTag(source=source, tags=tags_str, tags_levels=tags_levels)
                )

                STATS['eposeidon_sources'][source] += 1
                STATS['eposeidon_tags'][tags_str] += 1


def populate_code_du_travail_dict(json_file=os.path.join(BASE_DIR, 'dataset/code-du-travail-2018-01-01.json')):

    populate_eposeidon_tags_dict()

    with open(json_file) as json_data:
        data = json.load(json_data)
        inspect_code_du_travail_children(data['children'])


def inspect_code_du_travail_children(children):
    """
    Each children has the following structure and may contain 0 or more children
    with the same structure:
    {
        'type': 'article',
        'data': {
            'titre': 'Article D8254-7',
            'id': 'LEGIARTI000022357358',
            'section': 'LEGISCTA000018520564',
            'num': 'D8254-7',
            'etat': 'VIGUEUR',
            'date_debut': '2010-02-15',
            'date_fin': '2999-01-01',
            'type': 'AUTONOME',
            'nota': "<p>Décret n° 2009-1377 du 10 novembre 2009 article 7….</p>",
            'bloc_textuel': "<p><br/>Indépendamment de la procédure…</p>",
            'dossier': 'code_en_vigueur',
            'cid': 'LEGITEXT000006072050',
            'mtime': 1497984694
        },
        'children': […]
    }
    """

    for child in children:

        if child['type'] == 'article':

            STATS['count_article'] = STATS['count_article'] + 1

            article_num = child['data']['num']
            eposeidon_match = EPOSEIDON_TAGS_DICT.get(article_num)

            if not eposeidon_match:
                logging.debug('%s NOT FOUND in ePoseidon.', article_num)
                continue

            CODE_DU_TRAVAIL_DICT[article_num] = {
                'titre': child['data']['titre'],
                'id': child['data']['id'],
                'section': child['data']['section'],
                'num': child['data']['num'],
                'etat': child['data']['etat'],  # 'ABROGE_DIFF', 'VIGUEUR', 'VIGUEUR_DIFF', 'MODIFIE'
                'date_debut': child['data']['date_debut'],
                'date_fin': child['data']['date_fin'],
                'nota': child['data']['nota'],  # In HTML.
                'bloc_textuel': child['data']['bloc_textuel'],  # In HTML.
                'cid': child['data']['cid'],
                'tags': [
                    {
                        'source': item.source,
                        'tags': item.tags,
                        'tags_levels': item.tags_levels,
                    }
                    for item in eposeidon_match
                ]
            }

        # Recursion: inspect children, if any.
        inspect_code_du_travail_children(child.get('children', []))


def get_code_du_travail_dict():
    populate_code_du_travail_dict()
    return CODE_DU_TRAVAIL_DICT


def show_stats():

    if logging.getLogger().getEffectiveLevel() != logging.DEBUG:
        return

    logging.debug('-' * 80)
    logging.debug('ePoseidon sources stats:')
    for key in sorted(STATS['eposeidon_sources'], key=STATS['eposeidon_sources'].get, reverse=True):
        logging.debug('%5s - %s', STATS['eposeidon_sources'][key], key)

    logging.debug('-' * 80)
    logging.debug('ePoseidon tags stats:')
    for key in sorted(STATS['eposeidon_tags'], key=STATS['eposeidon_tags'].get, reverse=True):
        logging.debug('%5s - %s', STATS['eposeidon_tags'][key], key)

    logging.debug('-' * 80)
    logging.debug('ePoseidon tags sorted:')
    for key in sorted(STATS['eposeidon_tags'].keys()):
        logging.debug('%s', key)

    logging.debug('-' * 80)
    logging.debug('Number of articles: %s', STATS['count_article'])


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    populate_code_du_travail_dict()

    show_stats()
