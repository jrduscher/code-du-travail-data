import logging

from elasticsearch import Elasticsearch


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


def get_es_client():
    return Elasticsearch()


def test():
    logging.info('Get a very simple status on the health of the cluster.')
    es = get_es_client()
    logging.info(es.cluster.health())


if __name__ == '__main__':
    test()
