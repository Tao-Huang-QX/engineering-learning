# book-rag

RAG over part of a book (PDF source), built step by step by hand — the point is
to explore RAG setup, so the pipeline code is intentionally yours to write.

**Stack:** LlamaIndex (RAG core) · Docling (PDF parse + chunking) · pgvector via
podman (store) · LangGraph (agent, later). Directory is kebab-case; the import
package is snake_case (`book_rag`) — standard src-layout split.

## Setup

```bash
# 1. Python deps (shared workspace venv - no project-local venv)
pyenv activate engineering-learning
pip install -e ".[dev]"
# If the PyPI index response gets truncated (JSONDecodeError), retry or use a mirror:
#   pip install -e ".[dev]" -i https://pypi.tuna.tsinghua.edu.cn/simple

# 2. pgvector via podman (host port 5433)
# If docker.io is unreachable (registry ping EOF), pull via a mirror and retag
# so compose.yaml's image name resolves locally:
#   podman pull docker.m.daocloud.io/pgvector/pgvector:pg16
#   podman tag docker.m.daocloud.io/pgvector/pgvector:pg16 pgvector/pgvector:pg16
podman compose up -d
podman ps   # wait for book-rag-pgvector to be healthy

# 3. Local config
cp .env.example .env   # then edit: API key if you want ask/agent; defaults are fine for ingest/retrieve

# 4. Smoke test the installs
python -c "import docling, llama_index.core, langgraph, langchain; print('ok')"

# 5. Drop the book in (never committed - copyrighted)
cp /path/to/book-part.pdf data/
```

## Build order (write each step yourself)

| Step | Goal | Key pieces |
|------|------|-----------|
| 1 | Parse | `docling.document_converter.DocumentConverter` — PDF → markdown + structured doc |
| 2 | Chunk | `docling.chunking.HybridChunker` (tokenizer = your embed model, `merge_peers=True`); keep `{headings, page}` provenance per chunk |
| 3 | Inspect | Dump chunks to `out/`, eyeball for header/footer junk, heading paths, page metadata — before embedding anything |
| 4 | Store/embed | `llama_index.vector_stores.postgres.PGVectorStore.from_params(...)` + `VectorStoreIndex(nodes=..., storage_context=...)`; embed dim must match the model |
| 5 | Retrieve | `VectorIndexRetriever` top-k; format citations from `{headings, page}` |
| 6 | Eval | ~10 known questions → expected section; measure hit@k (JSON in `eval/questions.json`, gitignored) |
| 7 | Ask | Query engine + versioned prompt in `prompts/`; grounded answers with citations, honest "not in the book" |
| 8 | Agent | LangGraph `create_react_agent` with retrieval wrapped as a `search_book` tool |

## Conventions

- Python: workspace shared venv `engineering-learning` (pyenv); ruff via root `pyproject.toml`
- `data/`, `out/`, `.env`, `eval/questions.json` are gitignored — the book never gets committed
- Prompts, when you get there, are versioned files under `prompts/`, not string literals in code
