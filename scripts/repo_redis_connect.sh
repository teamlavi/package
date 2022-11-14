#!/usr/bin/env bash

kubectl exec -it deployment/repo-worker-redis -- /usr/local/bin/redis-cli
