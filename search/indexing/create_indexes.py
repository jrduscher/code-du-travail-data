import json
import logging
import os

import elasticsearch
from elasticsearch.helpers import bulk

from search import settings
from search.extraction.code_du_travail.cleaned_tags.data import CODE_DU_TRAVAIL_DICT
from search.extraction.fiches_ministere_travail.data import FICHES_MINISTERE_TRAVAIL
from search.extraction.fiches_service_public.data import FICHES_SERVICE_PUBLIC
from search.indexing import analysis
from search.indexing.mappings.code_du_travail import code_du_travail_mapping
from search.indexing.mappings.faq import faq_mapping
from search.indexing.mappings.fiches_ministere_travail import fiches_ministere_travail_mapping
from search.indexing.mappings.fiches_service_public import fiches_service_public_mapping


console = logging.StreamHandler()
formatter = logging.Formatter(fmt='[%(levelname)s - %(funcName)s] %(message)s')
console.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(console)
logger.setLevel(logging.INFO)


def get_es_client():
    """
    Configure the client for different environments.
    """
    hosts = [os.environ.get('ES_HOST')]
    return elasticsearch.Elasticsearch(hosts=hosts)


def drop_and_create_index(index_name, mapping_name, mapping):
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
                    'filter': analysis.filters,
                    'analyzer': analysis.analyzers,
                    'tokenizer': analysis.tokenizers,
                },
            },
        },
        'mappings': {
            mapping_name: mapping,
        },
    }
    es.indices.create(index=index_name, body=request_body)
    logger.info("Index `%s` created.", index_name)


def chunks(l, n):
    """
    Yield successive n-sized chunks from l.
    """
    for i in range(0, len(l), n):
        yield l[i:i+n]


def create_code_du_travail_documents(index_name, type_name):
    es = get_es_client()
    actions = []
    for val in CODE_DU_TRAVAIL_DICT.values():
        body = {
            'title': val['titre'],
            'text': val['bloc_textuel'],
            'url': val['url'],
            'path': [tag.path for tag in val['tags']],
        }
        actions.append({
            '_op_type': 'index',
            '_index': index_name,
            '_type': type_name,
            '_source': body,
        })
    for batch_action in chunks(actions, 1000):
        logger.info('Batch indexing %s documents', len(batch_action))
        bulk(es, batch_action)


def create_fiches_service_public_documents(index_name, type_name):
    es = get_es_client()
    actions = []
    for val in FICHES_SERVICE_PUBLIC:
        body = {
            'url': val['url'],
            'title': val['title'],
            'text': val['text'],
            'tags': val['tags'],
        }
        actions.append({
            '_op_type': 'index',
            '_index': index_name,
            '_type': type_name,
            '_source': body,
        })
    for batch_action in chunks(actions, 1000):
        logger.info('Batch indexing %s documents', len(batch_action))
        bulk(es, batch_action)


def create_fiches_ministere_travail_documents(index_name, type_name):
    es = get_es_client()
    actions = []
    for val in FICHES_MINISTERE_TRAVAIL:
        body = {
            'url': val['url'],
            'title': val['title'],
            'text': val['text'],
        }
        actions.append({
            '_op_type': 'index',
            '_index': index_name,
            '_type': type_name,
            '_source': body,
        })
    for batch_action in chunks(actions, 1000):
        logger.info('Batch indexing %s documents', len(batch_action))
        bulk(es, batch_action)


def create_faq_documents(index_name, type_name):
    es = get_es_client()
    actions = []
    with open(os.path.join(settings.BASE_DIR, 'dataset/faq.json')) as json_data:
        data = json.load(json_data)
        for val in data:
            body = {
                'title': val['question'],
                'text': f"{val['reponse']} {val['theme']} {val['branche']}",
            }
            actions.append({
                '_op_type': 'index',
                '_index': index_name,
                '_type': type_name,
                '_source': body,
            })
    for batch_action in chunks(actions, 1000):
        logger.info('Batch indexing %s documents', len(batch_action))
        bulk(es, batch_action)


if __name__ == '__main__':

    # We use 1 index by type because:
    # "Multiple types in the same index really shouldn't be used all that often
    # and one of the few use cases for types is parent child relationships."
    # See: https://www.elastic.co/blog/index-type-parent-child-join-now-future-in-elasticsearch

    name = 'code_du_travail'
    drop_and_create_index(index_name=name, mapping_name=name, mapping=code_du_travail_mapping)
    create_code_du_travail_documents(index_name=name, type_name=name)

    name = 'fiches_service_public'
    drop_and_create_index(index_name=name, mapping_name=name, mapping=fiches_service_public_mapping)
    create_fiches_service_public_documents(index_name=name, type_name=name)

    name = 'fiches_ministere_travail'
    drop_and_create_index(index_name=name, mapping_name=name, mapping=fiches_ministere_travail_mapping)
    create_fiches_ministere_travail_documents(index_name=name, type_name=name)

    name = 'faq'
    drop_and_create_index(index_name=name, mapping_name=name, mapping=faq_mapping)
    create_faq_documents(index_name=name, type_name=name)
