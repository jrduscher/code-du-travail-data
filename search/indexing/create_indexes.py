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
from search.indexing.mappings.all import all_mapping
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


def create_documents(body_data, index_name, type_name):
    es = get_es_client()
    actions = [
        {
            '_op_type': 'index',
            '_index': index_name,
            '_type': type_name,
            '_source': body,
        }
        for body in body_data
    ]
    for batch_action in chunks(actions, 1000):
        logger.info('Batch indexing %s documents', len(batch_action))
        bulk(es, batch_action)


def create_all_documents(index_name, type_name):
    body_data = []

    for val in CODE_DU_TRAVAIL_DICT.values():
        body_data.append({
            'source': 'code_du_travail',
            'text': val['bloc_textuel'],
            'title': val['titre'],
            'all_text': f"{val['titre']} {val['bloc_textuel']}",
            'path': [tag.path for tag in val['tags']],
            'url': val['url'],
        })

    for val in FICHES_SERVICE_PUBLIC:
        body_data.append({
            'source': 'fiches_service_public',
            'text': val['text'],
            'title': val['title'],
            'all_text': f"{val['title']} {val['text']}",
            'tags': val['tags'],
            'url': val['url'],
        })

    for val in FICHES_MINISTERE_TRAVAIL:
        body_data.append({
            'source': 'fiches_ministere_travail',
            'text': val['text'],
            'title': val['title'],
            'all_text': f"{val['title']} {val['text']}",
            'url': val['url'],
        })

    with open(os.path.join(settings.BASE_DIR, 'dataset/faq.json')) as json_data:
        data = json.load(json_data)
        for val in data:
            text = f"{val['reponse']} {val['theme']} {val['branche']}"
            body_data.append({
                'source': 'faq',
                'text': f"{text}",
                'title': val['question'],
                'all_text': f"val['question'] {text}",
            })

    return create_documents(body_data, index_name, type_name)


def create_code_du_travail_documents(index_name, type_name):
    body_data = [
        {
            'title': item['titre'],
            'text': item['bloc_textuel'],
            'url': item['url'],
            'path': [tag.path for tag in item['tags']],
        }
        for item in CODE_DU_TRAVAIL_DICT.values()
    ]
    return create_documents(body_data, index_name, type_name)


def create_faq_documents(index_name, type_name):
    with open(os.path.join(settings.BASE_DIR, 'dataset/faq.json')) as json_data:
        data = json.load(json_data)
        body_data = [
            {
                'title': item['question'],
                'text': f"{item['reponse']} {item['theme']} {item['branche']}",
            }
            for item in data
        ]
        return create_documents(body_data, index_name, type_name)


def create_fiches_ministere_travail_documents(index_name, type_name):
    body_data = [
        {
            'url': item['url'],
            'title': item['title'],
            'text': item['text'],
        }
        for item in FICHES_MINISTERE_TRAVAIL
    ]
    return create_documents(body_data, index_name, type_name)


def create_fiches_service_public_documents(index_name, type_name):
    body_data = [
        {
            'url': item['url'],
            'title': item['title'],
            'text': item['text'],
            'tags': item['tags'],
        }
        for item in FICHES_SERVICE_PUBLIC
    ]
    return create_documents(body_data, index_name, type_name)


if __name__ == '__main__':

    # Use 1 index by type, see:
    # https://www.elastic.co/blog/index-type-parent-child-join-now-future-in-elasticsearch

    name = 'all'
    drop_and_create_index(index_name=name, mapping_name=name, mapping=all_mapping)
    create_all_documents(index_name=name, type_name=name)

    name = 'code_du_travail'
    drop_and_create_index(index_name=name, mapping_name=name, mapping=code_du_travail_mapping)
    create_code_du_travail_documents(index_name=name, type_name=name)

    name = 'faq'
    drop_and_create_index(index_name=name, mapping_name=name, mapping=faq_mapping)
    create_faq_documents(index_name=name, type_name=name)

    name = 'fiches_ministere_travail'
    drop_and_create_index(index_name=name, mapping_name=name, mapping=fiches_ministere_travail_mapping)
    create_fiches_ministere_travail_documents(index_name=name, type_name=name)

    name = 'fiches_service_public'
    drop_and_create_index(index_name=name, mapping_name=name, mapping=fiches_service_public_mapping)
    create_fiches_service_public_documents(index_name=name, type_name=name)
