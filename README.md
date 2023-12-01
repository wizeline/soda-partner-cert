# SPC

Soda Parthership Certification

## Requirements

- Python >=3.10,<3.11
- Poetry >=1.7.0
- docker
- kubectl
- minikube
- helm

## Useful commands

```bash
# Read variables / secrets from `.env` file:
source .env

# Install dependencies via poetry project:
poetry install
```

### Dagster Commands

```bash
# Start dagster Server:
poetry run dagster dev

# Start dagster development server:
HERMES_ENVIRONMENT=development poetry run dagster dev
```

### dbt Commands

```bash
# Parse dbt project (Builds manifest.json file):
poetry run dbt parse \
    --project-dir ./spc/optimus \
    --profiles-dir ./

# Build dbt models in local environment:
poetry run dbt build \
    --project-dir ./spc/optimus \
    --profiles-dir ./

# Build dbt models in development environment:
poetry run dbt build \
    --target development \
    --project-dir ./spc/optimus \
    --profiles-dir ./
```

### Soda Commands

```bash

# Test connection to local environment:
poetry run soda test-connection \
    -d athena_local \
    -c ./spc/aphrodite/configuration.yml

# Test connection to development environment:
poetry run soda test-connection \
    -d athena_development \
    -c ./spc/aphrodite/configuration.yml

# Build soda ditribution object for el_kwh:
poetry run soda update-dro \
    -d athena_local \
    -n dro__ev_charging_reports__el_kwh \
    -c ./spc/aphrodite/configuration.yml \
    ./spc/aphrodite/distribution_reference.yml

# Run soda scan to local environment:
poetry run soda scan \
    -d athena_local \
    -c ./spc/aphrodite/configuration.yml \
    ./spc/aphrodite/checks.yml

# Run soda scan to development environment:
poetry run soda scan \
    -d athena_development \
    -c ./spc/aphrodite/configuration.yml \
    ./spc/aphrodite/checks.yml
```

### Kubernetes commands

```bash

# Start minikube cluster
minikube start

# Create soda agent / aphrodite namespace
kubectl create namespace aphrodite-agent

# Install soda agent in minikube cluster
helm install soda-agent soda-agent/soda-agent \
    --values ./spc/aphrodite/agent-values.yml \
    --namespace aphrodite-agent
```

## Sources

Data was pulled from [Kaggle](https://www.kaggle.com/datasets/anshtanwar/residential-ev-chargingfrom-apartment-buildings).
