# Agent Engineering — Context & Roadmap

Scope of this domain: prompt engineering, context engineering, and RAG —
learned by building real systems on the LangChain ecosystem, not toy examples.

## Core dependencies

| Layer | Choice | Role |
|-------|--------|------|
| Orchestration | **LangGraph** | Agent runtime: graphs, state, tool loops, human-in-the-loop |
| RAG core | **LlamaIndex** | Ingestion pipeline, indexes, retrievers, query engines |
| Building blocks | **LangChain** | Tool/agent primitives alongside LangGraph |
| Memory | **LangMem** | Long-term memory (semantic / episodic / procedural) on LangGraph |

## Learning tracks

1. **Prompt engineering** — system prompt design, few-shot, structured output, prompt versioning and testing.
2. **Context engineering** — what enters the window: context assembly, token budgets, compression/summarization, caching, tool-result trimming.
3. **RAG** ← *current focus*
   - Ingestion: parsing (PDF/book → clean text or markdown), chunking strategies for long-form prose
   - Indexing: embeddings, vector stores, hybrid search, metadata filtering
   - Retrieval: top-k, reranking, query rewriting, measuring retrieval quality
   - Generation: grounded answers with citations, honest "not in the book" behavior
4. **Agents** — tool use, ReAct loops, multi-step graphs, human-in-the-loop, agentic RAG.
5. **Memory** — LangMem in practice: what to store, when to forget, memory vs. retrieval.
6. **Evals** — golden question sets, LLM-as-judge, regression tests for prompts and retrieval.

## Current focus: RAG over a book

First task: take part of a book, split it, and build a working RAG pipeline over it.

- [x] **Pick RAG tooling** — decided 2026-11-16: **hybrid** — LlamaIndex as RAG core,
  LangGraph as orchestration. WeKnora/RAGFlow stay reference-only.
- [x] **Parser** — Docling (`DocumentConverter` + `HybridChunker`); MinerU is the fallback for hard scans
- [x] **Vector store** — pgvector via podman (`PGVectorStore`), host port 5433
- [ ] Book ingestion & splitting pipeline (chunking tuned for prose, not code)
- [ ] Index → retrieve → answer, with citations back to book sections
- [ ] Retrieval evaluation: does the right chunk come back for known questions?
- [ ] Expose retrieval as a LangGraph node → foundation for agentic RAG later

## Layout

```
agent-engineering/
  CONTEXT.md        ← this file: scope, roadmap, decisions
  CLAUDE.md         ← domain conventions
  book-rag/         ← first build: RAG over a PDF book (LlamaIndex + Docling + pgvector)
```

## Decision log

- 2026-11-16: Domain created. Core deps fixed (LangChain, LangGraph, LangMem).
- 2026-11-16: RAG tooling decided — build on LangChain (parser + local vector store).
  WeKnora/RAGFlow/LlamaIndex kept as reference implementations, not the core.
- 2026-11-16: Architecture refined to **hybrid** — LlamaIndex RAG core (product-level
  retrieval abstractions) + LangGraph orchestration. Source doc is a PDF book →
  Docling parser, pgvector store.
- 2026-11-16: `book-rag/` created directly under the domain (no projects/ level;
  kebab-case dir, snake_case package, shared `engineering-learning` venv).
  Dependencies scaffolded; pipeline code intentionally user-authored, step by step.
