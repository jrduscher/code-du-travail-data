# Temporary file that shows how to retrieve data from elasticsearch with curl.

# ---------------------------------------------------------------------------------------------------

# Find by _id
curl -XGET 'http://localhost:9200/code_du_travail_numerique/code_du_travail/WpH8uGIBlRNYkL9uQpaU?pretty'

# Use the URI request query.
curl -XGET 'http://localhost:9200/code_du_travail_numerique/code_du_travail/_search?q=titre:L1141&pretty'

# Same as above with the query DSL.
curl -H "Content-Type: application/json" -XGET 'http://localhost:9200/code_du_travail_numerique/code_du_travail/_search?pretty' -d '{
  "query": {
    "query_string": { "query": "titre:L1141" }
  }
}'

# With `_version` of the document.
curl -H "Content-Type: application/json" -XGET 'http://localhost:9200/code_du_travail_numerique/code_du_travail/_search?pretty' -d '{
  "version": true,
  "query": {
    "query_string": { "query": "titre:L1141" }
  }
}'

# With `min_score`.
curl -H "Content-Type: application/json" -XGET 'http://localhost:9200/code_du_travail_numerique/code_du_travail/_search?pretty' -d '{
  "min_score": 8,
  "query": {
    "query_string": { "query": "titre:L1141" }
  }
}'

# Choosing the fields that we want to return you can only return these fields if they are marked as stored in the mappings used to create the index, or if the _source field was used.
curl -H "Content-Type: application/json" -XGET 'http://localhost:9200/code_du_travail_numerique/code_du_travail/_search?pretty' -d '{
  "stored_fields": ["tags.path"],
  "query": {
    "query_string": { "query": "titre:L1141" }
  }
}'

# Hide source.
curl -H "Content-Type: application/json" -XGET 'http://localhost:9200/code_du_travail_numerique/code_du_travail/_search?pretty' -d '{
  "_source": false,
  "query": {
    "query_string": { "query": "titre:L1141" }
  }
}'

# Filter source fields.
curl -H "Content-Type: application/json" -XGET 'http://localhost:9200/code_du_travail_numerique/code_du_travail/_search?pretty' -d '{
  "_source": ["titre", "nota", "bloc_textuel"],
  "query": {
    "query_string": { "query": "titre:L1141" }
  }
}'

# ---------------------------------------------------------------------------------------------------

# Term query: matches the document that has a term in a given field - the exact, not analyzed term.
# Search for 'l1141' in lowercase instead of 'L1141': because 'L1141' becomes 'l1141' after analysis.
curl -H "Content-Type: application/json" -XGET 'http://localhost:9200/code_du_travail_numerique/code_du_travail/_search?pretty' -d '{
  "query": {
    "term": { "titre": "l1141" }
  }
}'

# Match all of the documents in the index.
curl -H "Content-Type: application/json" -XGET 'http://localhost:9200/code_du_travail_numerique/code_du_travail/_search?pretty' -d '{
  "query": {
    "match_all": {}
  }
}'

# Find all the documents with a certain type.
curl -H "Content-Type: application/json" -XGET 'http://localhost:9200/code_du_travail_numerique/_search?pretty' -d '{
  "query": {
    "type": { "value": "code_du_travail" }
  }
}'

# The match query: takes the values given in the query parameter, analyzes it,
# and constructs the appropriate query out of it.
curl -H "Content-Type: application/json" -XGET 'http://localhost:9200/code_du_travail_numerique/code_du_travail/_search?pretty' -d '{
  "query": {
    "match": { "titre": "Article L1141-1" }
  }
}'

curl -H "Content-Type: application/json" -XGET 'http://localhost:9200/code_du_travail_numerique/code_du_travail/_search?pretty' -d '{
  "query": {
    "match": {
        "titre": {"query": "Article L1141-", "operator": "and"}
    }
  }
}'

# ---------------------------------------------------------------------------------------------------

# Test analyzers regarding how tokens will be created.

curl -H "Content-Type: application/json" -XGET 'http://localhost:9200/_analyze?pretty' -d '{
  "analyzer": "english",
  "text": "Crime and Punishment"
}'

curl -H "Content-Type: application/json" -XGET 'http://localhost:9200/code_du_travail_numerique/_analyze?pretty' -d '{
  "field": "tags",
  "text": "/Santé Sécurité/Sécurité: Contrôle/Pénal/Infractions personne autre que employeur"
}'

curl -H "Content-Type: application/json" -XGET 'http://localhost:9200/code_du_travail_numerique/_analyze?pretty' -d '{
  "field": "num",
  "text": "R1227-7"
}'

curl -H "Content-Type: application/json" -XGET 'http://localhost:9200/_analyze?pretty' -d '{
  "analyzer": "keyword",
  "text": "R1227-7"
}'

# ---------------------------------------------------------------------------------------------------

# Filter by tag.

curl -H "Content-Type: application/json" -XGET 'http://localhost:9200/code_du_travail_numerique/code_du_travail/_search?pretty' -d '{
    "query": {
        "bool": {
            "must": {
                "match": {
                    "bloc_textuel": "interentreprises"
                }
            },
            "filter": {
                "term": {"tags": "/Santé Sécurité/Sécurité: Contrôle/Pénal/Infractions personne autre que employeur"}
            }
        }
    }
}'

# Find R1227-7 (because it has 2 tags).

curl -H "Content-Type: application/json" -XGET 'http://localhost:9200/code_du_travail_numerique/code_du_travail/_search?pretty' -d '{
  "query": {
    "term": { "num": "R1227-7" }
  }
}'

# Ensure that we can fetch R1227-7 with any of its tags.

curl -H "Content-Type: application/json" -XGET 'http://localhost:9200/code_du_travail_numerique/code_du_travail/_search?pretty' -d '{
  "query": {
    "term": {"tags": "/Contrat de travail/Contrat de Travail: Généralités, Embauche/Registre Unique du Personnel (RUP)> Registre Unique du Personnel (RUP) Pénal"}
  }
}'

curl -H "Content-Type: application/json" -XGET 'http://localhost:9200/code_du_travail_numerique/code_du_travail/_search?pretty' -d '{
  "query": {
    "term": {"tags": "/Contrat de travail/Contrat de Travail: Généralités, Embauche/Déclaration préalable à l\u0027embauche (DPAE)/Déclaration préalable à l\u0027embauche (DPAE) Pénal"}
  }
}'

# ---------------------------------------------------------------------------------------------------

# Count all tags

curl -H "Content-Type: application/json" -XGET 'http://localhost:9200/code_du_travail_numerique/code_du_travail/_search?pretty' -d '{
  "size": 0,
  "aggs": {
    "count_tags": {
      "cardinality": {
        "field": "tags"
      }
    }
  }
}'

# List all tags
# https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html
# https://qbox.io/blog/how-to-download-all-unique-terms-field-elasticsearch

curl -H "Content-Type: application/json" -XGET 'http://localhost:9200/code_du_travail_numerique/code_du_travail/_search?pretty' -d '{
  "size": 0,
  "aggs": {
    "distinct_tags": {
      "terms": {
        "field": "tags",
        "size": 100000
      }
    }
  }
}'
