import logging
import os

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
    'edge_ngram_filter': {
        'type': 'edge_ngram',
        'min_gram': 4,
        'max_gram': 20,
    },
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
    'edge_ngram_custom': {
        'type': 'custom',
        'char_filter': ['html_strip'],
        'tokenizer': 'standard',
        'filter': [
            'lowercase',
            'edge_ngram_filter',
        ],
    },
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
                'analyzer': 'keyword',
            },
            'titre': {
                'type': 'text',
                'analyzer': 'standard',
                'fields': {
                    'edge_ngram': {
                        'type': 'text',
                        'analyzer': 'edge_ngram_custom'
                    },
                    'french': {
                        'type': 'text',
                        'analyzer': 'french_custom'
                    },
                },
            },
            'nota': {
                'type': 'text',
                'analyzer': 'standard',
                'fields': {
                    'edge_ngram': {
                        'type': 'text',
                        'analyzer': 'edge_ngram_custom'
                    },
                    'french': {
                        'type': 'text',
                        'analyzer': 'french_custom'
                    },
                },
            },
            'bloc_textuel': {
                'type': 'text',
                'analyzer': 'standard',
                'fields': {
                    'edge_ngram': {
                        'type': 'text',
                        'analyzer': 'edge_ngram_custom'
                    },
                    'french': {
                        'type': 'text',
                        'analyzer': 'french_custom'
                    },
                },
            },
            'tags': {
                'type': 'text',
                'analyzer': 'path_analyzer_custom',
                'fielddata': True,
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
    Configure the client for different environments.
    """
    hosts = [os.environ.get('ES_HOST')]
    return elasticsearch.Elasticsearch(hosts=hosts)


def drop_and_create_index(index_name=INDEX_CODE_DU_TRAVAIL_NUMERIQUE):
    es = get_es_client()

    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
        logger.info("Index `%s` dropped.", index_name)

    request_body = {
        'settings': {
            'number_of_shards': 1,
            'number_of_replicas': 0,
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
            'tags': [tag.path for tag in val['tags']],
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
