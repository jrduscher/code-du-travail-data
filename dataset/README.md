# Sources des données

- FAQ
- Fichiers complets LegiFrance et/ou extraction Legilibre
- Tags fournis par ePoseidon
- BDCC : conventions collectives
- ngAccord : accords entreprise

# Fichiers

- `code_du_travail/`

    - `code-du-travail-2018-03-13.pdf` : PDF officiel du code du travail (legilibre)
    - `code-du-travail-2018-01-01.json` : code du travail au format JSON issu de [legi.py](https://github.com/Legilibre/legi.py)
    - `source_eposeidon/nomenclatures_*.xml` : taggages des articles du code du travail (depuis appli DGT ePoseidon)
    - `nomenclatures-*.json` : conversion des XML ePoseidon en JSON

- `faq.json` : questions fréquentes, reformulées par les services de renseignement des DIRECCTE

- `fiches_ministere_travail/fiches-min-travail.json` : extraction fiches [ministère du travail](http://travail-emploi.gouv.fr/mot/fiches-pratiques-du-droit-du-travail?max_articles=400)

- `fiches_service_public/fiches-sp-travail.json` : extraction fiches "vos droits" travail [service-public.fr](https://www.data.gouv.fr/fr/datasets/service-public-fr-guide-vos-droits-et-demarches-particuliers/)

- `thesaurus/TESS.json` : Thesaurus Travail Emploi Santé Solidarité


# Comment générer un JSON depuis un XML ePoseidon

Vérifier le chemin du XML dans la constante `INPUT_XML` du fichier `code_du_travail/eposeidon_script/index.js`, puis :

```
$ cd dataset/code_du_travail/eposeidon_script
$ npm --version
5.10.0
$ node --version
v9.11.2
$ npm install
$ node index.js > ../nomenclatures-`date +%Y%m%d`.json
```
