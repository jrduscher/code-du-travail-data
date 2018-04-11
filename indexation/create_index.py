import logging

import elasticsearch
from elasticsearch.helpers import bulk

from indexation.parse_code_du_travail import CODE_DU_TRAVAIL_DICT


console = logging.StreamHandler()
formatter = logging.Formatter(fmt='[%(levelname)s - %(funcName)s] %(message)s')
console.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(console)
logger.setLevel(logging.INFO)


INDEX_NAME = 'code_du_travail_numerique'


filters = {
    'french_elision': {
        'type': 'elision',
        'articles_case': True,
        'articles': [
            'l', 'm', 't', 'qu', 'n', 's',
            'j', 'd', 'c', 'jusqu', 'quoiqu',
            'lorsqu', 'puisqu',
        ],
    },
    'french_stop': {
        'type': 'stop',
        'stopwords': '_french_',
    },
    'french_keywords': {
        'type': 'keyword_marker',
        'keywords': ['Exemple'],
    },
    'french_stemmer': {
        'type': 'stemmer',
        'language': 'light_french',
    },
}


analyzers = {
    'french_custom': {
        'tokenizer': 'standard',
        'char_filter': ['html_strip'],
        'filter': [
            'french_elision',
            'lowercase',
            'french_stop',
            'french_keywords',
            'french_stemmer',
        ],
    },
}


# A `mappings` object defines how the data looks in Elasticsearch.
# It contains 1 or more `types`.
mappings = {

    'code_du_travail': {
        'properties': {
            'num': {
                'type': 'text',
                'analyzer': 'french_custom',
            },
            'titre': {
                'type': 'text',
                'analyzer': 'french_custom',
            },
            'nota': {
                'type': 'text',
                'analyzer': 'french_custom',
            },
            'bloc_textuel': {
                'type': 'text',
                'analyzer': 'french_custom',
            },
            # 'tags': {
            #     'type': 'object',
            #     'index': 'not_analyzed',
            # },
            'id': {
                'type': 'text',
                'index': False,
            },
            'section': {
                'type': 'text',
                'index': False,
            },
            'etat': {
                'type': 'text',
                'index': False,
            },
            'date_debut': {
                'type': 'date',
                'format': 'yyyy-MM-dd',
                'index': False,
            },
            'date_fin': {
                'type': 'date',
                'format': 'yyyy-MM-dd',
                'index': False,
            },
            'cid': {
                'type': 'text',
                'index': False,
            },
        },
    },

}


def get_es_client():
    """
    Will be used to configure the client for different environments.
    """
    return elasticsearch.Elasticsearch()


def drop_and_create_index(index_name=INDEX_NAME):
    es = get_es_client()

    try:
        es.indices.delete(index=index_name)
        logger.info("Index `%s` dropped.", index_name)
    except elasticsearch.NotFoundError:
        # This happens when the index did not previously exist.
        pass

    request_body = {
        'settings': {
            'index': {
                'analysis': {
                    'filter': filters,
                    'analyzer': analyzers,
                },
            },
        },
        'mappings':  {
            'code_du_travail': mappings['code_du_travail'],
        },
    }
    es.indices.create(index=index_name, body=request_body)
    logger.info("Index `%s` created.", index_name)


def test():
    logger.info('Get a very simple status on the health of the cluster.')
    es = get_es_client()
    logger.info(es.cluster.health())


def chunks(l, n):
    """
    Yield successive n-sized chunks from l.
    """
    for i in range(0, len(l), n):
        yield l[i:i+n]


def create_code_du_travail_documents(index_name=INDEX_NAME):
    es = get_es_client()
    actions = []
    for val in CODE_DU_TRAVAIL_DICT.values():
        body = {
            'num': val['num'],
            'titre': val['titre'],
            'nota': val['nota'],
            'bloc_textuel': val['bloc_textuel'],
            'id': val['id'],
            'section': val['section'],
            'etat': val['etat'],
            'date_debut': val['date_debut'],
            'date_fin': val['date_fin'],
            'cid': val['cid'],
            # 'tags': val['tags'],
        }
        # print(val['tags'][0].source)
        # print(val['tags'][0].tags)
        # print(val['tags'][0].tags_levels)
        actions.append({
            '_op_type': 'index',
            '_index': index_name,
            '_type': 'code_du_travail',
            '_source': body,
        })

    for batch_action in chunks(actions, 1000):
        logger.info('Batch indexing %s documents', len(batch_action))
        bulk(es, batch_action)


if __name__ == '__main__':
    drop_and_create_index()
    create_code_du_travail_documents()
