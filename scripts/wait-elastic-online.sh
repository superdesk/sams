#!/usr/bin/env sh

host='sams:9200'

function getHealStatus()
{
    # wait for ES status to turn to Green
    health="$(curl -fsSL "$host/_cat/health?h=status")"

    # trim whitespace (otherwise we'll have "green ")
    health="$(echo "$health" | sed -r 's/^[[:space:]]+|[[:space:]]+$//g')"
}

getHealStatus
until [ "$health" = 'green' ]; do
    getHealStatus
#    health="$(curl -fsSL "$host/_cat/health?h=status")"
#    health="$(echo "$health" | sed -r 's/^[[:space:]]+|[[:space:]]+$//g')" # trim whitespace (otherwise we'll have "green ")
    >&2 echo "Elasticsearch is unavailable - sleeping"
    sleep 1
done

echo "Elasticsearch is now available"
