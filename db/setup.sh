#!/usr/bin/env bash

set -o errexit

echo "start setting up a database"

echo "create a database named tapa"
if [[ "$uname" == "Darwin" ]]; then
    sudo -u $(whoami) dropdb -e tapa
    sleep 1
    sudo -u $(whoami) createdb -O $(whoami) -e tapa
else
    sudo -u postgres dropdb -e tapa
    sleep 1
    sudo -u postgres createdb -O postgres -e tapa
fi

echo "load a schema"
psql tapa < db/schema.sql

echo "add constraints"
psql tapa < db/constraint.sql

echo "add pre-populate sample data"
psql tapa < db/data.sql

echo "finish setting up a database"
