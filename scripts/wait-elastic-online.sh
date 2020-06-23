#!/usr/bin/env sh

host='localhost:9200'

function getHealthStatus()
{
    # wait for ES status to turn to Green
    health="$(curl -fsSL "$host/_cat/health?h=status")"

    # trim whitespace (otherwise we'll have "green ")
    health="$(echo "$health" | sed -r 's/^[[:space:]]+|[[:space:]]+$//g')"
}

getHealthStatus
until [ "$health" = 'green' ]; do
    getHealthStatus
    >&2 echo "Elasticsearch is unavailable - sleeping"
    sleep 1
done

echo "Elasticsearch is now available"
