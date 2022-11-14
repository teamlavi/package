#!/usr/bin/env bash

kubectl exec -it statefulset/lavi-worker-db -- /usr/bin/psql postgresql://admin@localhost:5432/cvedb
