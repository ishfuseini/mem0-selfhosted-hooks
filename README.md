# mem0-agent-hook

A provider-agnostic memory core for a **self-hosted** [Mem0](https://mem0.ai) instance.

Self-hosted Mem0 has no MCP server, so memory has to be reached through the Python SDK
directly. Mem0's own reference material for this is the OpenAI Agents SDK cookbook, which
welds the memory operations to one framework's types — follow it and the logic only works
inside that framework. This project keeps the three memory operations in a single module with
**no agent-framework imports**, so the same core is callable from any agent stack, LLM
provider, or plain script.

> **Status:** in development. The core is written but not yet verified against a live
> instance, and the project is not yet installable as a dependency. See
> [`docs/tasks/v1-core-library.md`](docs/tasks/v1-core-library.md) for the remaining work.

## The core API

`mem0_core.py` exposes three async functions. `user_id` is optional and falls back to
`DEFAULT_USER_ID` (`"default_user"`).

```python
import asyncio
from mem0_core import add_memory, search_memory, get_all_memory

async def main():
    await add_memory("I prefer dark mode", user_id="ish")
    print(await search_memory("ui preferences", user_id="ish"))
    print(await get_all_memory(user_id="ish"))

asyncio.run(main())
```

| Function | Returns |
| --- | --- |
| `add_memory(content, user_id=None)` | Confirmation string |
| `search_memory(query, user_id=None)` | Matching memory text, one per line |
| `get_all_memory(user_id=None)` | All memory text, one per line |

### Invariants

These are what make the module portable. Breaking one re-couples the core to a framework and
defeats the point of the project:

1. `user_id` is an explicit argument — never read from a framework context object.
2. Plain Python return types only. No framework-specific result or tool types.
3. Zero agent-framework imports in the core module.
4. All Mem0 client calls are confined to this one module.

Framework integrations belong in thin adapters that call into the core — an adapter translates
calling conventions, it does not contain memory logic. None are built yet.

## Setup

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

Configuration is read from the environment via `python-dotenv`. Create a `.env` with:

- `MEM0_API_KEY` — API key for your Mem0 instance
- `MEM0_HOST` — URL of your self-hosted instance

`.env` is gitignored and must stay that way.

## Documentation

| Path | Contents |
| --- | --- |
| `docs/architecture/` | The PRD — scope, goals, and non-goals |
| `docs/tasks/` | Active implementation plans |
| `docs/guides/` | Operational and usage guidance |
| `docs/api/` | Function contracts and integration notes |

`AGENTS.md` and `PROJECT-CONVENTIONS.md` govern how changes are made to this repository.
