#!/usr/bin/env bash

docker compose exec -T backend-db psql "postgresql://user:password@localhost:5432/cvedb" < db_backup.sql
