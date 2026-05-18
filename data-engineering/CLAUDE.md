# Data Engineering

## Structure
```
pipelines/         Self-contained ETL/ELT projects
sql/               Query patterns, optimization, window functions
spark/             PySpark jobs with cluster sizing notes
infrastructure/    Docker, Airflow DAGs, dbt models, Terraform
```

## Pipeline Conventions

- Each pipeline is a directory with:
  ```
  pipeline_name/
    pipeline.py      Entry point (orchestration logic)
    extract.py       Source connectors
    transform.py     Business logic / transformations
    load.py          Sink connectors
    config.yaml      Pipeline configuration
    tests/           pytest
  ```
- Use generators and streaming where possible — avoid loading full datasets into memory
- Configs are external (YAML/env), never hardcoded in source
- Include a data quality check step in every pipeline

## SQL Conventions

- Keywords: lowercase (select, from, where, join)
- Trailing commas for column lists
- Common table expressions (CTEs) over subqueries
- Every query file includes an input/output schema comment
- Organize by pattern: `sql/window_functions/`, `sql/joins/`, `sql/optimization/`

## Spark Conventions

- Each job is a self-contained `.py` file or small package
- Include cluster sizing estimate as a comment at the top:
  ```python
  # Cluster: N workers, M cores each, X GB RAM each
  # Input: ~Y GB
  ```
- Use DataFrame API, not RDD, unless there's a specific reason
- Avoid `collect()` on large DataFrames

## Infrastructure

- Docker Compose for local stack (Airflow, PostgreSQL, Spark)
- dbt models follow standard dbt project structure
- Terraform modules for any cloud resources
