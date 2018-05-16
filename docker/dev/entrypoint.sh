#!/bin/sh
set -e

while ! curl "http://${ES_HOST}:9200/_cat/health?h=status"
do
    echo "Elasticsearch instance not available: still trying to connect."
    sleep 1
done
echo "Elasticsearch instance available: connected successfully."

/bin/sh -c "trap : TERM INT; while sleep 3600; do :; done"

exec "$@"
