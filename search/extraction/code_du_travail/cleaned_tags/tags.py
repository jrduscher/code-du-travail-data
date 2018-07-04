"""
Build a dict where each key is a reference of an article of the code du travail
and each value is its associated tag, e.g.:

    {
        'L1254-1': 'Contrat de travail > Autres cas de mise à disposition > Portage salarial > Portage salarial',
        'L1254-2': 'Contrat de travail > Autres cas de mise à disposition > Portage salarial > Portage salarial',
        …
    }

"""
import os
import csv

from search.settings import BASE_DIR


# This file contains tag humanly renamed. Source:
# https://github.com/SocialGouv/code-du-travail-explorer/blob/5071d9/src/data/themes.js
TAGS_CSV = os.path.join(BASE_DIR, 'dataset/code_du_travail/themes.csv')


TAGS_DICT = {}


def get_cleaned_tags(csv_file=TAGS_CSV):

    with open(csv_file) as csv_data:
        tag_reader = csv.reader(csv_data, delimiter='\t')
        for row in tag_reader:
            tag = row[1].strip()
            articles = [article.strip() for article in row[2].split(';')]
            for article in articles:
                TAGS_DICT[article] = tag


get_cleaned_tags()
