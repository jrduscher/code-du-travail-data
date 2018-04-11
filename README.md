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

### Paramétrage du fichier `.env`

Le répertoire `code-du-travail-data` doit figurer dans votre `PYTHONPATH`.

```
PYTHONPATH=/your/path/to/code-du-travail-data
ou
PYTHONPATH=.
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

# List of all indexes (indices).
curl -XGET 'localhost:9200/_cat/indices?v'

# Get information about one index.
curl -XGET 'http://localhost:9200/code_du_travail_numerique/?pretty'

# Retrieve mapping definitions for an index or type.
curl -XGET 'http://localhost:9200/code_du_travail_numerique/_mapping/?pretty'
curl -XGET 'http://localhost:9200/code_du_travail_numerique/_mapping/code_du_travail?pretty'

# Search explicitly for documents of a given type within the code_du_travail index.
curl -XGET 'http://localhost:9200/code_du_travail_numerique/code_du_travail/_search?pretty'
```

## Commandes Python

```shell
$ pipenv run python indexation/create_index.py
$ pipenv run python indexation/parse_code_du_travail.py
```
