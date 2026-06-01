# Engineering Learning

Hands-on engineering practice and interview preparation monorepo.

**Target roles:** Data Engineering Manager, Software Engineering Manager, Senior Engineer.  
**Approach:** Learn by building — no toy examples, real patterns.

## Directory Structure

```
leetcode/           Algorithm & data structure practice (Python)
  algorithms/       Solutions organized by technique
  data-structures/  Implementations and patterns
  templates/        Reusable solution scaffolds

full-stack/         End-to-end application development
  backend/          Python (FastAPI/Flask) and Java (Spring Boot)
  frontend/         React + TypeScript
  projects/         Combined full-stack applications

data-engineering/   Data infrastructure and pipeline work
  pipelines/        ETL/ELT pipeline projects
  sql/              Query patterns, window functions, optimization
  spark/            PySpark jobs and distributed processing
  infrastructure/   Docker, Airflow, dbt, Terraform configs

shared/             Cross-domain utilities and helpers
  utils/            Shared Python utilities
```

## Quick Start

### Prerequisites

- Python 3.13+
- [Poetry](https://python-poetry.org/) for dependency management

### Setup

```bash
# Clone and navigate to the project
git clone <repo-url>
cd engineering-learning

# Install dependencies with Poetry
poetry install

# Activate the virtual environment (optional)
poetry shell
```

### Running Code

```bash
# LeetCode solutions
poetry run python leetcode/algorithms/hash-map/0001_two_sum.py

# Linting
poetry run ruff check .
poetry run ruff format .
```

## Tech Stack

| Domain | Primary | Secondary |
|--------|---------|-----------|
| LeetCode | Python 3 | — |
| Backend | Python (FastAPI) | Java (Spring Boot) |
| Frontend | React + TypeScript | — |
| Data Engineering | Python (PySpark, dbt) | SQL |
| Infrastructure | Docker | Airflow, Terraform |

## Conventions

### LeetCode

- File naming: `{problem_number}_{slug}.py` (e.g., `0001_two_sum.py`)
- Solutions organized by primary technique/pattern
- Every solution includes complexity analysis
- See [leetcode/CLAUDE.md](leetcode/CLAUDE.md) for full workflow

### Git

- Branch: `feature/<thing>`, `fix/<thing>`, `learn/<topic>`
- Commits: imperative mood, present tense ("add two-pointer solution for 3Sum")

### Code Quality

- Python linting: `ruff` (configured in `pyproject.toml`)
- Line length: 100 characters
- Target Python version: 3.13

## Progress

- **LeetCode:** 30/148 problems solved (see [leetcode/PROGRESS.md](leetcode/PROGRESS.md))
- **Roadmap:** Following [labuladong's algorithm framework](https://labuladong.online/zh/roadmap/algo/) (see [leetcode/QUEUE.md](leetcode/QUEUE.md))

## License

MIT
