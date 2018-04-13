import logging

import elasticsearch
from elasticsearch.helpers import bulk

from indexation.code_du_travail_load import CODE_DU_TRAVAIL_DICT


console = logging.StreamHandler()
formatter = logging.Formatter(fmt='[%(levelname)s - %(funcName)s] %(message)s')
console.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(console)
logger.setLevel(logging.INFO)


INDEX_CODE_DU_TRAVAIL_NUMERIQUE = 'code_du_travail_numerique'
TYPE_CODE_DU_TRAVAIL = 'code_du_travail'


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
    'path_analyzer_custom': {
        'tokenizer': 'tags',
    },
}

tokenizers = {
    'tags': {
        'type': 'path_hierarchy',
    },
}


# A `mappings` object defines how the data looks in Elasticsearch.
# It contains 1 or more `types`.
mappings = {

    TYPE_CODE_DU_TRAVAIL: {
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
            'tags': {
                'type': 'text',
                'fields': {
                    'name': {
                        'type': 'text',
                        'index': False,
                    },
                    'path': {
                        'type': 'text',
                        'analyzer': 'path_analyzer_custom',
                        'store': True,
                    },
                }
            },
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


def drop_and_create_index(index_name=INDEX_CODE_DU_TRAVAIL_NUMERIQUE):
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
                    'tokenizer': tokenizers,
                },
            },
        },
        'mappings':  {
            TYPE_CODE_DU_TRAVAIL: mappings[TYPE_CODE_DU_TRAVAIL],
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


def create_code_du_travail_documents(index_name=INDEX_CODE_DU_TRAVAIL_NUMERIQUE):
    es = get_es_client()
    actions = []
    for val in CODE_DU_TRAVAIL_DICT.values():
        body = {
            'num': val['num'],
            'titre': val['titre'],
            'nota': val['nota'],
            'bloc_textuel': val['bloc_textuel'],
            'tags': val['tags'][0].path,
            'id': val['id'],
            'section': val['section'],
            'etat': val['etat'],
            'date_debut': val['date_debut'],
            'date_fin': val['date_fin'],
            'cid': val['cid'],
        }
        actions.append({
            '_op_type': 'index',
            '_index': index_name,
            '_type': TYPE_CODE_DU_TRAVAIL,
            '_source': body,
        })

    for batch_action in chunks(actions, 1000):
        logger.info('Batch indexing %s documents', len(batch_action))
        bulk(es, batch_action)


if __name__ == '__main__':
    drop_and_create_index()
    create_code_du_travail_documents()