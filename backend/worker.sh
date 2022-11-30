#!/usr/bin/env bash

set -e

# Check if env vars set
if [[ -z "${QUEUE_NAME}" ]]
then
    echo "QUEUE_NAME env var is not set"
    exit 1
fi

if [[ -z "${REDIS_HOST}" ]]
then
    echo "REDIS_HOST env var is not set"
    exit 1
fi

REDIS_URL="redis://${REDIS_HOST}:${REDIS_PORT:-6379}/0"
echo "Attempting to connect to $REDIS_URL"

# Wait for redis to pop up
echo "Waiting for redis"
for i in $(seq 1 15)
do
    tmp=0
    python3 -c "import redis; redis.Redis.from_url('${REDIS_URL}').ping()" || tmp=$?
    if [ $tmp -eq 0 ]
    then
        echo "Redis ping successful"
        break
    else
        echo "No successful ping yet, $i seconds elapsed"
    fi
    sleep 1
done

if [ $tmp -ne 0 ]
then
    echo "Timeout waiting for ping"
    exit 1
fi

# Start the worker
rq worker --with-scheduler --url "$REDIS_URL" --worker-ttl 300 "$QUEUE_NAME"
