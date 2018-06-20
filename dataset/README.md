# Sources des données

- FAQ
- Fichiers complets LegiFrance et/ou extraction Legilibre
- Tags fournis par ePoseidon
- BDCC : conventions collectives
- ngAccord : accords entreprise

# Fichiers

- `code-du-travail-2018-03-13.pdf` : PDF officiel du code du travail (legilibre)
- `code-du-travail-2018-01-01.json` : code du travail au format JSON issu de [legi.py](https://github.com/Legilibre/legi.py)
- `source_eposeidon/nomenclatures_*.xml` : taggages des articles du code du travail (depuis appli DGT ePoseidon)
- `nomenclatures-*.json` : conversion des XML ePoseidon en JSON
- `faq.json` : 55 questions fréquentes, reformulées par les services de renseignement des DIRECCTE
- `fiches-sp-travail.json` : extraction fiches "vos droits" travail [service-public.fr](https://www.data.gouv.fr/fr/datasets/service-public-fr-guide-vos-droits-et-demarches-particuliers/)

# Comment générer un JSON depuis un XML ePoseidon

Vérifier le chemin du XML dans la constante `INPUT_XML` du fichier `source_eposeidon/index.js`, puis :

```
$ cd source_eposeidon
$ npm --version
5.8.0
$ node --version
v9.11.1
$ npm install
$ node index.js > ../nomenclatures-`date +%Y%m%d`.json
```
