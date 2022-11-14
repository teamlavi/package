#!/usr/bin/env bash

kubectl exec -it deployment/lavi-worker-redis -- /usr/local/bin/redis-cli
