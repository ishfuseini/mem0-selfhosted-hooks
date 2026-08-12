# PRD: mem0-agent-hook

**Status:** Draft
**Scope:** V1 — core library only

---

## 1. Problem

The Mem0 instance backing this work is self-hosted, so the hosted MCP server is not an option.
Memory has to be reached through the Mem0 Python SDK directly.

Mem0's own reference material for this is the OpenAI Agents SDK cookbook, which welds the
memory operations to one framework's types — `function_tool`, `Agent`, `RunContextWrapper`.
Following it produces memory logic that only works inside that one framework. Using memory
from a second stack (a Claude Code hook, LangChain, a plain script) means writing the same
three Mem0 calls again, with the same bugs available to be reintroduced each time.

The cost is duplication, and a memory layer that can't move between projects.

## 2. Goals

- **One memory core**, callable from any agent framework, LLM provider, or plain script.
- **Reusable across projects** without dragging a framework dependency along with it.
- **Small.** Readable in one sitting. A Mem0 SDK change should be a single-file edit.

## 3. Non-goals (V1)

- Adapter implementations — OpenAI Agents SDK, Claude Code hooks, LangChain. Named in §7 as
  future phases; not built here.
- An MCP server implementation.
- Public/open-source packaging, a versioning policy, or API stability guarantees.
- Memory operations beyond the three below — no update, delete, graph memory, or custom
  categories.

## 4. Users

One user, many projects. The consumer is the user's own code and agents, not third parties.
This shapes the tradeoffs: no backwards-compatibility burden, no external API contract, but
the module does need to be genuinely portable between repos.

## 5. Functional requirements — the core API

`mem0_core.py` exposes three async functions. All take `user_id` explicitly, defaulting to
`DEFAULT_USER_ID` (`"default_user"`) when omitted.

| Function | Signature | Returns |
| --- | --- | --- |
| Add | `add_memory(content: str, user_id: str \| None = None) -> str` | Confirmation string |
| Search | `search_memory(query: str, user_id: str \| None = None) -> str` | Matching memory text, one per line |
| Get all | `get_all_memory(user_id: str \| None = None) -> str` | All memory text, one per line |

### Invariants

These are the reusability contract. They are what make the module portable, and they are
mirrored in `PROJECT-CONVENTIONS.md`:

1. `user_id` is an explicit argument — never read from a framework context/request object.
2. Returns plain Python types only. No framework-specific result or tool types.
3. Zero agent-framework imports in the core module.
4. All Mem0 client calls are confined to this one module. Nothing else constructs an
   `AsyncMemoryClient`.

Breaking any of these re-couples the core to a framework and defeats the point of the project.

## 6. Configuration

Loaded from the environment via `python-dotenv`:

- `MEM0_API_KEY` — API key for the Mem0 instance
- `MEM0_HOST` — URL of the self-hosted instance

`.env` is gitignored and must stay that way. See §9 for a known mismatch between these names
and what `.env` currently contains.

## 7. Future phases (not committed)

Candidate adapters, each a thin translation layer over the core, each to be specced
separately before any work starts:

- **OpenAI Agents SDK** — wrap the three functions with `@function_tool` and map the SDK's
  context object to a `user_id`.
- **Claude Code hook** — a script matching the hook stdin/stdout JSON contract
  (e.g. `UserPromptSubmit`) that stores and injects memory automatically.

An adapter translates calling conventions. It does not contain memory logic.

## 8. Success criteria

- The core imports and runs with **no agent-framework package installed**.
- A new project can use memory by importing the module and calling the functions — nothing
  else to wire up.
- Adding support for a new framework requires **no edit to `mem0_core.py`**.

## 9. Open questions

- **`.env` key mismatch (blocker for live use). Resolved (T1).** `.env` now defines
  `MEM0_API_KEY` and `MEM0_HOST`, matching what `mem0_core.py` reads. Both resolve to
  non-`None` values at client construction.
- **No automated validation.** No test runner, linter, or type checker is configured.
  Validation is manual until that changes.
- **Cross-project reuse mechanism undecided.** Path import, local package install, or git
  dependency — the choice affects future packaging and has not been made.
