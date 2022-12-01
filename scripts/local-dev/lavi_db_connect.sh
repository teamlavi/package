#!/usr/bin/env bash

docker compose exec backend-db psql "postgresql://user:password@localhost:5432/cvedb"
