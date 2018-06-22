import json
import logging
import os

import elasticsearch
from elasticsearch.helpers import bulk

from indexation import settings
from indexation.code_du_travail.cleaned_tags.data import CODE_DU_TRAVAIL_DICT
from indexation.elastic import analysis
from indexation.elastic.mappings.code_du_travail import code_du_travail_mapping
from indexation.elastic.mappings.faq import faq_mapping
from indexation.elastic.mappings.fiches_service_public import fiches_service_public_mapping
from indexation.fiches_service_public.data import FICHES_SERVICE_PUBLIC


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
            'sous_theme': val['sous_theme'],
            'title': val['title'],
            'text': val['text'],
            'tags': val['tags'],
            'refs': val['refs'],
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
                'question': val['question'],
                'reponse': val['reponse'],
                'theme': val['theme'],
                'branche': val['branche'],
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

    # Code du travail.
    drop_and_create_index(
        index_name=settings.ES_CODE_DU_TRAVAIL,
        mapping_name=settings.ES_CODE_DU_TRAVAIL,
        mapping=code_du_travail_mapping
    )
    create_code_du_travail_documents(
        index_name=settings.ES_CODE_DU_TRAVAIL,
        type_name=settings.ES_CODE_DU_TRAVAIL
    )

    # Fiches service public.
    drop_and_create_index(
        index_name=settings.ES_FICHES_SERVICE_PUBLIC,
        mapping_name=settings.ES_FICHES_SERVICE_PUBLIC,
        mapping=fiches_service_public_mapping
    )
    create_fiches_service_public_documents(
        index_name=settings.ES_FICHES_SERVICE_PUBLIC,
        type_name=settings.ES_FICHES_SERVICE_PUBLIC
    )

    # FAQ.
    drop_and_create_index(
        index_name=settings.ES_FAQ,
        mapping_name=settings.ES_FAQ,
        mapping=faq_mapping
    )
    create_faq_documents(
        index_name=settings.ES_FAQ,
        type_name=settings.ES_FAQ
    )
