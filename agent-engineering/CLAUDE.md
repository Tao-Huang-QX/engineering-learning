# Agent Engineering

Prompt engineering, context engineering, and RAG practice on the LangChain ecosystem.
Scope, roadmap, and current focus live in [CONTEXT.md](CONTEXT.md) — update it as decisions land.

## Stack

- Python 3 in the shared pyenv virtualenv `engineering-learning` (no per-project venvs)
- **LangGraph** (orchestration), **LlamaIndex** (RAG core), **LangChain** (tooling), **LangMem** (memory)
- Docling for document parsing; pgvector via podman as the vector store
- Ruff via the root `pyproject.toml`; same docstring convention as the rest of the workspace

## Conventions

- Builds are self-contained directories directly under `agent-engineering/` (e.g. `book-rag/`):
  kebab-case directory, snake_case import package under `src/`, each with its own `README.md`
- Prompts are versioned artifacts: checked-in files under a build's `prompts/`, not string literals buried in code
- **Never commit book/document source files** — copyrighted content stays in a local `data/` directory that is gitignored; commit only small synthetic fixtures if a sample is needed for tests
- API keys and model config go in `.env` (gitignored); commit a `.env.example` instead
