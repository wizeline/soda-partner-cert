# soda-partner-cert

Soda Parthership Certification

## Useful commands

Load data into DuckDB file:

```bash
duckdb ./minerva.duck < ./sql/load.sql
```

Test connections:

```bash
soda test-connection -d minerva -c ./spc/soda/configuration.yml -V
```

Run checks:

```bash
soda scan -d minerva -c ./spc/soda/configuration.yml ./spc/soda/checks.yml
```
