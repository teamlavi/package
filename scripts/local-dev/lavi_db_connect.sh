#!/usr/bin/env bash

docker-compose exec lavi-worker-db psql postgresql://user:password@localhost:5432/cvedb
