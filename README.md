# SPC

Soda Parthership Certification

## Useful commands

Read variables from `.env` file:

```bash
export $(cat ./.env | xargs)
```

Start dagster Server:

```bash
poetry run dagster dev
```

Build dbt models:

```bash
poetry run dbt build --project-dir ./spc/optimus --profiles-dir ./
```

Test SODA connections:

```bash
poetry run soda test-connection -d athena -c ./spc/soda/configuration.yml -V
```

Run SODA checks:

```bash
poetry run soda scan -d athena -c ./spc/soda/configuration.yml ./spc/soda/checks.yml
```

## Sources

Data was pulled from [Kaggle](https://www.kaggle.com/datasets/anshtanwar/residential-ev-chargingfrom-apartment-buildings).
