#!/usr/bin/env bash

if [ "$SERVICES" == "true" ]; then
    docker-compose -f .travis-docker-compose.yml up -d
    while ! curl -sfo /dev/null 'http://localhost:9200/'; do echo -n '.' && sleep .5; done
fi

if [ "$START_SAMS" == "true" ]; then
    cd src/server
    (nohup honcho start &)
    cd ../../
fi
