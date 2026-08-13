# PROJECT-CONVENTIONS.md

## Project

`mem0-agent-hook` is a Python library that wraps a self-hosted Mem0
instance behind a provider/agent-agnostic core API.

The core exposes plain async functions for adding, searching, and
retrieving memories. It has no dependency on any specific agent
framework (OpenAI Agents SDK, Claude Code hooks, LangChain, etc.).
Framework-specific integrations are thin adapters built on top of the
core, not the other way around.

This document defines project-specific implementation conventions.
General agent behavior, scope control, review requirements, and
documentation structure are defined in `AGENTS.md`.

---

## Runtime and Package Management

- Runtime: Python 3.13+
- Package manager: uv
- Package: `mem0ai`
- Config loading: `python-dotenv`

### Package Management

Use `uv` exclusively.

Install dependencies:

    uv sync

Add a runtime dependency:

    uv add <package>

Add a development dependency:

    uv add --dev <package>

Do not use pip, poetry, or conda directly against this project.

Commit `uv.lock` whenever dependency state changes.

Do not add dependencies when the existing core module or standard
library adequately solves the problem.

---

## Architecture

### Core

`mem0_core.py` is the framework-agnostic layer. It owns:

- the `AsyncMemoryClient` instance and its configuration
- `add_memory(content, user_id)`
- `search_memory(query, user_id)`
- `get_all_memory(user_id)`

Core functions must:

- accept `user_id` as an explicit argument, never read it from a
  framework-specific context/request object
- return plain Python types (str, dict, list) — never
  framework-specific result/tool types
- have no import of any agent-framework package (`agents`,
  `langchain`, etc.)

### Adapters

Framework integrations (e.g. an OpenAI Agents SDK tool wrapper, a
Claude Code hook script) live outside `mem0_core.py` and call into it.
An adapter should only translate between a framework's calling
convention and the core functions — it should not contain memory
logic of its own.

Do not add framework-specific parameters or types to core functions
to accommodate an adapter. If an adapter needs something the core
doesn't provide, extend the core's plain interface instead.

---

## Application Commands

Run the CLI entry point:

    uv run python hello.py

Run any script in the project:

    uv run python <script>.py

---

## Validation

- Test runner: `pytest` (with `pytest-asyncio`, `asyncio_mode = "auto"`)
- Linter: `ruff`

Run before reporting a task complete:

    uv run pytest
    uv run ruff check

Both must pass. `tests/conftest.py` patches `mem0.AsyncMemoryClient`
before `mem0_core` is first imported, so importing `mem0_core` and
running the test suite never makes a network call — the module
otherwise validates its API key against the live host at import time.

No type checker is configured yet.

---

## Python Conventions

- Prefer explicit type hints on function signatures, especially at
  the core module's public boundary (`mem0_core.py`).
- Use `str | None` (not `Optional[str]`) per the `from __future__
  import annotations` style already used in this repo.
- Keep core functions small and single-purpose; one Mem0 operation
  per function.
- Do not catch and swallow exceptions from the Mem0 client — let
  failures surface to the caller unless the task specifically calls
  for error handling.

---

## Configuration and Secrets

Secrets must not be committed to Git. `.env` is gitignored — keep it
that way.

Required environment variables:

- `MEM0_API_KEY` — Mem0 API key
- `MEM0_HOST` — URL of the self-hosted Mem0 instance

Do not introduce new environment variable names for the same value
(the repo has previously accumulated an unused, differently-cased
`mem0_API_KEY`/`mem0_ENDPOINT` pair — don't repeat that pattern).

Never place real credentials in source code, documentation, tests, or
task documents.

---

## External Integrations

Mem0 is the only external service this project talks to. Treat it as
a system boundary:

- All Mem0 client calls go through `mem0_core.py` — no other module
  should import `AsyncMemoryClient` directly.
- Keep the core's public functions decoupled from Mem0 SDK-specific
  types (`filters` dict shape, response envelopes) where practical, so
  a future SDK change is a one-file update.

---

## Documentation

Documentation structure is defined by `AGENTS.md`.

Project documentation lives under:

    docs/
    ├── tasks/
    ├── architecture/
    ├── guides/
    └── api/

Use:

- `docs/tasks/` for active implementation plans
- `docs/architecture/` for durable system design and decisions
  (e.g. the core/adapter split)
- `docs/guides/` for operational and usage guidance
- `docs/api/` for the core module's function contracts and any
  adapter-specific integration notes

Do not create additional documentation categories unless existing
ones cannot reasonably represent the content.

---

## Deployment

This project is a library/hook, not a deployed service. There is no
CI/CD pipeline, container build, or hosted runtime to manage as part
of implementation tasks unless a task explicitly introduces one.

---

## Dependency Changes

Before introducing a new dependency:

1. Determine whether the standard library or `mem0_core.py` already
   provides the capability.
2. Prefer actively maintained dependencies.
3. Avoid adding a second package that overlaps an existing one (e.g.
   another Mem0 client, another env-loading library).

Dependency upgrades should not be bundled into unrelated feature work.

---

## Definition of Project Validation

For a normal change to this project, successful validation means:

1. The change imports and runs under `uv run python <entry point>`
   without error.
2. Any new/changed core function has been manually exercised against
   the configured Mem0 instance, or the inability to do so is
   reported explicitly.
3. `pyproject.toml`/`uv.lock` are consistent with actual imports used.

Additional validation may be required by the task or `AGENTS.md`.
