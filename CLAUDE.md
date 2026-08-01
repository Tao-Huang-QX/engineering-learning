# Engineering Learning Workspace

Hands-on engineering practice and interview preparation monorepo.

**Target roles:** Data Engineering Manager, Software Engineering Manager, Senior Engineer.
**Approach:** Learn by building — no toy examples, real patterns.

## Directory Map

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

## Tech Stack

| Domain | Primary | Secondary |
|--------|---------|-----------|
| LeetCode | Python 3 | — |
| Backend | Python (FastAPI) | Java (Spring Boot) |
| Frontend | React + TypeScript | — |
| Data Engineering | Python (PySpark, dbt) | SQL |
| Infrastructure | Docker | Airflow, Terraform |

Adding new languages or domains: update this file, add a domain-level CLAUDE.md, and follow existing conventions.

## Conventions

### Python (all domains)

- Every function docstring follows this format:

```python
"""
{One-line summary.}

Args:
    param_name: Type and description
    ...

Returns:
    Return type and description
"""
```

- Include `Args: None` and `Returns:` even when there are no parameters — be consistent
- Modules should be self-contained with inline tests or a `__main__` block
- Ruff for linting and formatting (`ruff check .` / `ruff format .`); config in `pyproject.toml`

### Full-Stack

- Backend projects live in `backend/{language}/` with their own venv/gradle setups
- Frontend projects use Vite + React + TypeScript, live in `frontend/react-typescript/`
- Combined projects go in `projects/` with `backend/` and `frontend/` subdirectories
- API design: RESTful, proper status codes, input validation at the boundary
- Each project gets its own README with setup instructions

### Data Engineering

- Pipelines are self-contained directories with a `pipeline.py` entry point
- SQL files use lowercase keywords and trailing commas
- Spark jobs include cluster sizing notes in comments
- Infrastructure configs are versioned and environment-parameterized

### Git

- Branch: `feature/<thing>`, `fix/<thing>`, `learn/<topic>`
- Commits: imperative mood, present tense ("add two-pointer solution for 3Sum")
- Commit message format (Conventional Commits / Angular style):

```
[type]: [subject]

[bullet points for changes]

Co-Authored-By: Claude <noreply@anthropic.com>
```

Example:
```
Add Subtree of Another Tree solution, update progress

- Add 0572_subtree_of_another_tree.py with iterative DFS approach
- Fix slice boundaries in 0105 preorder construction (left subtree)
- Update PROGRESS.md with solved entry (57/120 completed)

Co-Authored-By: Claude <noreply@anthropic.com>
```

- No large generated files, no secrets, no virtualenvs/node_modules

### Domain-Specific Conventions

- **LeetCode:** see [leetcode/CLAUDE.md](leetcode/CLAUDE.md) for problem template, quiz workflow, review checklist, and placement rules
- **Full-Stack / Data Engineering:** conventions above; add a domain CLAUDE.md when the sub-project grows

## Claude's Role

This workspace is a partnership. Claude operates in these modes:

### Review Mode
When you share a solution, Claude checks:
- Correctness (edge cases, off-by-one, null/empty inputs)
- Complexity (time and space — is it optimal?)
- Readability (naming, structure, unnecessary abstraction)
- Pattern fit (is this the right technique for this problem class?)

### Build Mode
When scaffolding or building, Claude:
- Follows the conventions in this file
- Creates working, runnable code (not stubs)
- Sets up tests, configs, and READMEs
- Uses existing patterns before inventing new ones

### Mock Interview Mode
Claude can conduct:
- **Coding interviews**: Timed, with problem statement, hints, and feedback
- **System design interviews**: Architecture, trade-offs, scaling
- **Behavioral/management interviews**: STAR-format, leadership scenarios

### Teaching Mode
When asked to explain, Claude:
- Connects concepts to problems you've already solved in this repo
- Explains the WHY, not just the WHAT
- Uses concrete examples from the codebase

### Quiz Generation (LeetCode)

Two flows; see [leetcode/CLAUDE.md](leetcode/CLAUDE.md) for the full workflow:
1. **Skill (`leetcode-quiz`)** — when the user hands in a specific problem description
2. **Default** — generate the next quiz from the queue (cues: "next", "quiz me", etc.)

## Workflow Recipes

### "Let's solve a LeetCode problem"
See [leetcode/CLAUDE.md](leetcode/CLAUDE.md) for the complete quiz workflow.

### "Let's build a full-stack feature"
1. Define the feature and scope
2. Claude scaffolds backend endpoint + frontend component
3. Build iteratively, Claude reviews each step

### "Let's design a data pipeline"
1. Define source, transformations, sink
2. Claude helps design the pipeline structure
3. Implement in `data-engineering/pipelines/<name>/`

### "Give me a mock interview"
1. Specify type: coding / system design / behavioral
2. Specify target company or role level if relevant
3. Claude runs a timed session with realistic constraints

### "Review this solution"
Just paste your code. Claude checks against the review criteria above.

### "Explain <concept>"
Claude explains with references to problems or patterns already in this repo.
