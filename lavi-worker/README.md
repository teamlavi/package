# LAVI Worker

The backend API supporting LAVI's functionality.


# Running

### In remote cluster (preferred)

TODO

### Local docker container

```bash
docker build --target=main --tag=lavi-worker .
docker run -p 8080:8080 lavi-worker uvicorn --port=8080 --host=0.0.0.0 lavi_worker.main:app
```

### Directly

```bash
pip3 install --upgrade -r requirements.txt
uvicorn --port=8080 lavi_worker.main:app
```


# Development

### In remote cluster (preferred)

TODO

### Directly

```bash
pip3 install --upgrade -r requirements.txt
uvicorn --port=8080 lavi_worker.main:app
```

# Testing

### In remote cluster (preferred)

TODO

### Local docker container

```bash
docker build --target=main --tag=lavi-worker .
docker run -p 8080:8080 lavi-worker bash tests/lint.sh
```

### Directly

```bash
pip3 install --upgrade -r requirements.txt
bash tests/lint.sh
```
