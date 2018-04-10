# Code du travail - Data

Ce dépôt de code contient un prototype d'indexation du code du travail.

## Installation de l'environnement de développement

### Création de l'environnement Python isolé

Avec Python 3.6 et [`pipenv`](https://github.com/pypa/pipenv) :

```bash
$ pipenv --python 3.6
$ pipenv install
$ pipenv install --dev
```

### Elasticsearch avec Docker

- Version: `6.2.x`
- Doc: https://www.elastic.co/guide/en/elasticsearch/reference/6.2/docker.html
- Python binding: http://elasticsearch-py.readthedocs.io/

#### Installation

```shell
$ docker pull docker.elastic.co/elasticsearch/elasticsearch:6.2.3
```

#### Lancement

```shell
$ docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:6.2.3
```

#### Tests

```shell
# Cluster health check.
$ curl -XGET 'localhost:9200/_cat/health?v'

# List of nodes in the cluster.
$ curl -XGET 'localhost:9200/_cat/nodes?v'
```

## Commandes Python

```shell
$ pipenv run python index/create_index.py
$ pipenv run python index/parse_code_du_travail.py
```
