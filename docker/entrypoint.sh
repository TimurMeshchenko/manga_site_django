#!/bin/bash

until nc -z $DB_HOST $DB_PORT; do
  echo "Waiting for Postgresql to be available..."
  sleep 1
done

exec "$@"
