# Useful commands

## General use

```bash
# Read variables / secrets from `.env` file:
source .env

# Install dependencies via poetry project:
poetry install
```

## Dagster

```bash
# Start dagster Server:
poetry run dagster dev

# Start dagster development server:
HERMES_ENVIRONMENT=development poetry run dagster dev
```

## dbt

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
poetry run dbt build --target development \
    --project-dir ./spc/optimus \
    --profiles-dir ./
```

## Soda

```bash
# Test connection to local environment:
poetry run soda test-connection -d athena_local \
    -c ./spc/aphrodite/configuration.yml

# Test connection to development environment:
poetry run soda test-connection -d athena_development \
    -c ./spc/aphrodite/configuration.yml

# Build soda ditribution object for el_kwh:
poetry run soda update-dro -d athena_local \
    -n dro__ev_charging_reports__el_kwh \
    -c ./spc/aphrodite/configuration.yml \
    ./spc/aphrodite/distribution_reference.yml

# Run soda scan to local environment:
poetry run soda scan -d athena_local \
    -c ./spc/aphrodite/configuration.yml \
    ./spc/aphrodite/checks.yml

# Run soda scan to development environment:
poetry run soda scan -d athena_development \
    -c ./spc/aphrodite/configuration.yml \
    ./spc/aphrodite/checks.yml

# Ingest dbt test results:
soda ingest dbt -d athena_dev \
    -c ./spc/aphrodite/configuration.yml \
    --dbt-artifacts ./spc/optimus/target
```

## Kubernetes

```bash
# Add soda repo to helm (Done once):
helm repo add soda-agent https://helm.soda.io/soda-agent/

# Start minikube cluster:
minikube start

# ALT: Start minikube cluster with limited resources:
minikube start --cpus='2' --memory='4096m'

# Create soda-agent / aphrodite namespace
kubectl create namespace aphrodite

# Create secret for gcp service account credentials
kubectl create secret generic gcloud-sa-creds -n aphrodite \
    --from-file service_account.json=$GCP_SA_JSON_PATH

# Install soda agent in minikube cluster
helm install soda-agent soda-agent/soda-agent -n aphrodite \
    --values ./spc/aphrodite/agent-values.yml \
    --set soda.agent.id=$SODA_AGENT_ID \
    --set soda.apikey.id=$SODA_AGENT_API_KEY_ID \
    --set soda.apikey.secret=$SODA_AGENT_API_KEY_SECRET

# Monitor agent status
kubectl get pods -n aphrodite

# Follow soda orchestrator logs (helps debug api errors)
kubectl logs -f -n aphrodite \
    -l agent.soda.io/component=orchestrator

# Follow soda worker logs (helps debug scan errors)
kubectl logs -f -n aphrodite \
    -l agent.soda.io/component=scanlauncher

# Delete / stop the soda agent
helm delete soda-agent -n aphrodite

# Stop minikube cluster
minikube stop
```
