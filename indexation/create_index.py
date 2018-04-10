import logging

import elasticsearch
# Elasticsearch, NotFoundError

# from indexation.parse_code_du_travail import get_code_du_travail_dict


console = logging.StreamHandler()
formatter = logging.Formatter(fmt='[%(levelname)s - %(funcName)s] %(message)s')
console.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(console)
logger.setLevel(logging.INFO)


INDEX_NAME = 'code_du_travail_numerique'


filters = {}


analyzers = {}


mappings = {

    'code_du_travail': {
        'properties': {
            'titre': {
                'type': 'text',
                # 'index': 'not_analyzed',
            },
            'id': {
                'type': 'text',
                # 'index': 'not_analyzed',
            },
            'section': {
                'type': 'text',
                # 'index': 'not_analyzed',
            },
            'num': {
                'type': 'text',
                # 'index': 'not_analyzed',
            },
            'etat': {
                'type': 'text',
                # 'index': 'not_analyzed',
            },
            'date_debut': {
                'type': 'text',  # 2010-02-15
                # 'index': 'not_analyzed',
            },
            'date_fin': {
                'type': 'text',  # 2010-02-15
                # 'index': 'not_analyzed',
            },
            'nota': {
                'type': 'text',
                # 'index': 'not_analyzed',
            },
            'bloc_textuel': {
                'type': 'text',
                # 'index': 'not_analyzed',
            },
            'cid': {
                'type': 'text',
                # 'index': 'not_analyzed',
            },
            # 'tags': {
            #     'type': 'object',
            #     'index': 'not_analyzed',
            # },
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


# code_du_travail_dict = get_code_du_travail_dict()
# for key, val in code_du_travail_dict.items():
#     logger.info(val['titre'])
#     logger.info(val['num'])


def test():
    logger.info('Get a very simple status on the health of the cluster.')
    es = get_es_client()
    logger.info(es.cluster.health())


if __name__ == '__main__':
    drop_and_create_index()
