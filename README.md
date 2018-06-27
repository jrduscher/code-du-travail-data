# Code du travail - Data

Ce dépôt de code permet d'indexer différentes sources de données relatives au Code du travail dans Elasticsearch.

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

## Extraction

Exemple de commandes pour vérifier les données qui seront indexées dans Elasticsearch.

```shell
# Pour vérifier les données du code du travail :

# 1) Données accompagnées des "tags" extraits de ePoseidon :
$ docker exec -ti code-du-travail-data-python pipenv run python search/extraction/code_du_travail/eposeidon_tags/data.py -v

# 2) Données accompagnées des "tags" renommés humainement (depuis l'extraction ePoseidon) :
$ docker exec -ti code-du-travail-data-python pipenv run python search/extraction/code_du_travail/cleaned_tags/data.py -v

# Pour vérifier les données des fiches services public :

$ docker exec -ti code-du-travail-data-python pipenv run python search/extraction/fiches_service_public/data.py -v
```

## Indexation

```shell
# Pour peupler l'index d'Elasticsearch :
$ docker exec -ti code-du-travail-data-python pipenv run python search/indexing/create_indexes.py
```
