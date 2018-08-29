# Code du travail - Data

Ce dépôt de code permet d'indexer différentes sources de données relatives au Code du travail dans Elasticsearch.

## Installation de l'environnement de développement

Créez un fichier `.env` (utilisé par Docker) :

```shell
PYTHONPATH=.

# Use the Docker elasticsearch's hostname: defaults to the container's name if not specified.
ES_HOST=code-du-travail-data-elasticsearch
```

Puis :

```bash
$ docker-compose up
```

## Indexation des données

Lors du premier lancement d'Elasticsearch ou d'une modification des données indexées, vous avez besoin d'indexer les données dans la base :

```shell
$ docker exec -ti code-du-travail-data-python pipenv run python search/indexing/create_indexes.py
```

## Pour lancer un shell Docker

```shell
$ docker exec -ti code-du-travail-data-python /bin/sh
$ docker exec -ti code-du-travail-data-elasticsearch /bin/sh
```

## Extraction : vérifier les données qui seront indexées dans Elasticsearch

Il est possible de visualiser les données qui seront indexées dans Elasticsearch dans un shell en utilisant l'option `verbose` des commandes :

```shell
# Pour vérifier les données du code du travail :
# 1) Données accompagnées des "tags" extraits de ePoseidon :
$ docker exec -ti code-du-travail-data-python pipenv run python search/extraction/code_du_travail/eposeidon_tags/data.py -v
# 2) Données accompagnées des "tags" renommés humainement :
$ docker exec -ti code-du-travail-data-python pipenv run python search/extraction/code_du_travail/cleaned_tags/data.py -v

# Pour vérifier les données des fiches Ministère du Travail :
$ docker exec -ti code-du-travail-data-python pipenv run python search/extraction/fiches_ministere_travail/data.py -v

# Pour vérifier les données des fiches services public :
$ docker exec -ti code-du-travail-data-python pipenv run python search/extraction/fiches_service_public/data.py -v

# Pour vérifier les données des synonymes :
$ docker exec -ti code-du-travail-data-python pipenv run python search/extraction/synonyms/data.py -v
```
