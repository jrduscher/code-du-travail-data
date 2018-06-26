# Code du travail - Data

Ce dépôt de code contient un prototype d'indexation du code du travail.

## Installation de l'environnement de développement

Créez un fichier `.env` (utilisé par Docker) :

```shell
PYTHONPATH=.

# The Docker elasticsearch's hostname. Defaults to the container's name if not specified.
ES_HOST=code-du-travail-data-elasticsearch
```

Puis :

```bash
$ docker-compose up
```

## Pour lancer un shell Docker

```shell
$ docker exec -ti code-du-travail-data-python /bin/sh
```

## Indexation

```shell

# Pour vérifier les données du code du travail qui seront indexées dans Elasticsearch :

# 1) à partir des "tags" extraits de ePoseidon:
$ docker exec -ti code-du-travail-data-python pipenv run python search/extraction/code_du_travail/eposeidon_tags/data.py -v

# 2) ou à partir des "tags" renommés humainement à partir de l'extraction ePoseidon:
$ docker exec -ti code-du-travail-data-python pipenv run python search/extraction/code_du_travail/cleaned_tags/data.py -v

# Pour peupler l'index d'Elasticsearch :
$ docker exec -ti code-du-travail-data-python pipenv run python search/indexing/create_indexes.py
```
