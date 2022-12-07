#!/usr/bin/env bash

docker compose exec backend-db pg_dumpall -d "postgresql://user:password@localhost:5432/cvedb" > db_backup.sql
