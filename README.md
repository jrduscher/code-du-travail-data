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

## Commandes Python

D'abord lancer un shell Docker :

```shell
$ docker exec -ti code-du-travail-data-python /bin/sh
```

Puis :

```shell
# Pour vérifier les données du code du travail qui seront indexées dans Elasticsearch :
$ pipenv run python indexation/code_du_travail_load.py -v

# Pour peupler l'index d'Elasticsearch :
$ pipenv run python indexation/create_index.py
```
