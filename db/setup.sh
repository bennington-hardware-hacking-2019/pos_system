#!/usr/bin/env bash

# if there is an error, stop everything
set -o errexit

echo "start setting up a database"

echo "create a database named tapa"
# test what the operating system is
if [[ "$OSTYPE" == "darwin"* ]]; then
    sudo -u $(whoami) dropdb -e tapa
    sleep 1
    sudo -u $(whoami) createdb -O $(whoami) -e tapa
else
    # this will be our raspberry pi
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
