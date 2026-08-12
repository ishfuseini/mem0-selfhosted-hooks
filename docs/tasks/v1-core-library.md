# Task Plan: V1 Core Library

**Source:** `docs/architecture/PRD.md`
**Decomposition depth:** 2 (Standard)
**Status:** Ready for implementation

Five tasks, five PRs. Each task is one PR gate.

```
T1 ──┐
     ├──> T3 ──> T4 ──> T5
T2 ──┘
```

T1 and T2 are independent of each other and may run in parallel. T3 requires both.

Decisions already made, not to be relitigated during implementation:

- Cross-project reuse is a **git dependency with `mem0_core.py` kept flat** (no `src/` package
  restructure). Resolves PRD §9's third open question.
- Git baseline (initial commit, remote) is handled by the human before T1 begins.

---

## T1 — Reconcile environment configuration

**Purpose**
PRD §9 blocker. `.env` defines `mem0_API_KEY` / `mem0_ENDPOINT`, but `mem0_core.py:11` reads
`MEM0_API_KEY` / `MEM0_HOST`. Both resolve to `None`, so the client cannot reach the
self-hosted instance at all.

**Dependencies:** none.

**PR boundary:** alone. Small and independently revertable.

**Acceptance criteria**
- `.env` uses `MEM0_API_KEY` and `MEM0_HOST`; the old lowercase pair is removed.
- `.env` remains gitignored. No `.env.example` — the variable names are documented in
  `README.md` instead (decided: not worth a second file for two variables).
- Both values resolve to non-`None` at client construction.
- PRD §9 first open question marked resolved.

**Relevant files:** `.env` (uncommitted), `docs/architecture/PRD.md`

---

## T2 — Validation tooling and core unit tests

**Purpose**
`AGENTS.md` §Definition of Done requires validation before work is complete; this project has
no test runner, linter, or type checker. Resolves PRD §9's second open question.

**Dependencies:** none.

**PR boundary:** tooling and tests ship together. A pytest config with no tests is inert, and
neither half would be reverted without the other.

**Acceptance criteria**
- `pytest`, `pytest-asyncio`, and `ruff` added as dev dependencies via `uv add --dev`.
- Unit tests covering all three functions in `mem0_core.py:16-32`, with the Mem0 client
  stubbed. **No network calls in the test suite.**
- Both the `DEFAULT_USER_ID` fallback path and an explicit `user_id` are covered.
- An **invariant test** enforcing PRD §5 invariant 3: parse `mem0_core.py`'s AST and fail if
  any import matches an agent-framework denylist (`agents`, `langchain`, `llama_index`, …).
  Use AST parsing rather than `sys.modules` inspection so the result is deterministic and
  independent of what else the test session imported.
- `uv run pytest` and `uv run ruff check` both pass.
- `PROJECT-CONVENTIONS.md` §Validation rewritten. It currently states no tooling is configured
  and instructs that the chosen tools and run commands be recorded there by whichever task
  introduces them — this is that task.

**Relevant files:** `pyproject.toml`, `tests/test_mem0_core.py` (new), `PROJECT-CONVENTIONS.md`

---

## T3 — Verify the core against the live instance

**Purpose**
The three functions have never been executed against a real Mem0 instance. Their response and
filter shapes are unconfirmed against the pinned `mem0ai 2.0.18`.

**Dependencies:** T1 (configuration must work), T2 (harness for any regression test).

**PR boundary:** alone. May land as a no-op code change if the shapes already match.

**Known risk to confirm**
Mem0's documentation shows two different filter forms — `filters={"user_id": x}` and
`filters={"AND": [{"user_id": x}]}` — and the `{"results": [...]}` response envelope assumed at
`mem0_core.py:26` and `mem0_core.py:32` varies by API version. Either could break
`search_memory` or `get_all_memory` at runtime.

**Acceptance criteria**
- All three functions executed against the self-hosted instance.
- An add → search round-trip returns the stored content.
- Any shape mismatch fixed in `mem0_core.py`, with a regression test covering it.
- If no fix proved necessary, that is stated explicitly in the PR rather than left implied.

**Relevant files:** `mem0_core.py`, `tests/test_mem0_core.py`

---

## T4 — Make the project installable as a git dependency

**Purpose**
PRD §2 goal, "reusable across projects." Implements the decided resolution to PRD §9's third
open question.

**Dependencies:** T3. Do not publish a module whose runtime behavior is unverified.

**PR boundary:** alone.

**Acceptance criteria**
- `[build-system]` added (hatchling). `pyproject.toml` currently has no build system, so the
  project is not buildable and `uv add git+…` would fail against it.
- Wheel configuration explicitly includes `mem0_core.py` as a top-level module.
- `hello.py` deleted. It is `uv init` boilerplate that would otherwise ship inside the wheel;
  in scope here as a packaging artifact, not as unrelated cleanup.
- From a scratch venv **outside this repository**, installing the project and running
  `from mem0_core import add_memory` succeeds.
- PRD §9 updated with the decision and its rationale.

**Relevant files:** `pyproject.toml`, `hello.py` (delete), `docs/architecture/PRD.md`

---

## T5 — Usage documentation

**Purpose**
`AGENTS.md` requires durable behavior changes to be reflected in documentation. `README.md` is
currently 0 bytes, and `docs/api/` and `docs/guides/` are empty.

**Dependencies:** T4. Install instructions depend on the packaging outcome.

**PR boundary:** alone.

**Acceptance criteria**
- `README.md`: what the project is, how to install it as a git dependency, and a minimal usage
  example.
- `docs/api/core-api.md`: the three function contracts — signatures, return shapes,
  `DEFAULT_USER_ID` behavior, and the PRD §5 invariants an adapter author must respect.
- `docs/guides/setup.md`: environment configuration against a self-hosted Mem0 instance.
- No real credentials in any of it.
- Every PRD §9 open question either resolved or explicitly restated as still open.

**Relevant files:** `README.md`, `docs/api/core-api.md` (new), `docs/guides/setup.md` (new)

---

## Out of scope

Per PRD §3: no adapter implementations (OpenAI Agents SDK, Claude Code hook, LangChain), no
MCP server, no public packaging or versioning policy, and no memory operations beyond the
three defined. If work on any of these surfaces during implementation, report it separately
rather than absorbing it into the current task (`AGENTS.md` §Scope Control).
