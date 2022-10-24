# LAVI Worker

The backend API supporting LAVI's functionality.


# Running

## In remote cluster (preferred)

TODO

## Local docker container

From inside [lavi-worker/container](./container) directory.
```bash
docker build --target=main --tag=lavi-worker .
docker run -p 8080:8080 lavi-worker uvicorn --port=8080 --host=0.0.0.0 lavi_worker.main:app
```

## Directly

From inside [lavi-worker/container](./container) directory.
```bash
pip3 install --upgrade -r requirements.txt
uvicorn --port=8080 lavi_worker.main:app
```


# Development

## In remote cluster (preferred)

TODO

## Directly

From inside [lavi-worker/container](./container) directory.
```bash
pip3 install --upgrade -r requirements.txt
uvicorn --port=8080 lavi_worker.main:app
```

# Testing

## In remote cluster (preferred)

TODO

## Local docker container

From inside [lavi-worker/container](./container) directory.
```bash
docker build --target=main --tag=lavi-worker .
docker run -p 8080:8080 lavi-worker bash tests/lint.sh
```

## Directly

From inside [lavi-worker/container](./container) directory.
```bash
pip3 install --upgrade -r requirements.txt
bash tests/lint.sh
```
