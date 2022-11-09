# LAVI Worker

The backend API supporting LAVI's functionality.

#random comment
# Running

### In remote cluster (preferred)

From [repository root](../):
```bash
garden deploy lavi-worker
kubectl port-forward --namespace=<your namespace> service/lavi-worker 8080:80
```

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

From [repository root](../):
```bash
garden deploy --dev-mode lavi-worker
kubectl port-forward --namespace=<your namespace> service/lavi-worker 8080:80
```

### Directly

```bash
pip3 install --upgrade -r requirements.txt
uvicorn --port=8080 lavi_worker.main:app
```

# Linting / Unit Testing

### In remote cluster (preferred)

From [repository root](../):
```bash
garden test lavi-worker-ctr
```

### Local docker container

```bash
docker build --target=main --tag=lavi-worker .
docker run lavi-worker bash tests/lint.sh
docker run lavi-worker pytest -v tests/unit
```

### Directly

```bash
pip3 install --upgrade -r requirements.txt
export PYTHONPATH=$PYTHONPATH:.
bash tests/lint.sh
pytest -v tests/unit
```
