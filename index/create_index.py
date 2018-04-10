import logging

from elasticsearch import Elasticsearch


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


mapping_code_du_travail = {
    "properties": {
        "titre": {
            "type": "string",
            # "index": "not_analyzed",
        },
        "id": {
            "type": "string",
            # "index": "not_analyzed",
        },
        "section": {
            "type": "string",
            # "index": "not_analyzed",
        },
        "num": {
            "type": "string",
            # "index": "not_analyzed",
        },
        "etat": {
            "type": "string",
            # "index": "not_analyzed",
        },
        "date_debut": {
            "type": "string",  # 2010-02-15
            # "index": "not_analyzed",
        },
        "date_fin": {
            "type": "string",  # 2010-02-15
            # "index": "not_analyzed",
        },
        "nota": {
            "type": "string",
            # "index": "not_analyzed",
        },
        "bloc_textuel": {
            "type": "string",
            # "index": "not_analyzed",
        },
        "cid": {
            "type": "string",
            # "index": "not_analyzed",
        },
        # "tags": {
        #     "type": "object",
        #     "index": "not_analyzed",
        # },
    },
}


def get_es_client():
    return Elasticsearch()


def test():
    logging.info('Get a very simple status on the health of the cluster.')
    es = get_es_client()
    logging.info(es.cluster.health())


if __name__ == '__main__':
    test()
