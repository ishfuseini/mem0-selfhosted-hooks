from __future__ import annotations

import ast
from pathlib import Path
from unittest.mock import AsyncMock

import pytest

import mem0_core

AGENT_FRAMEWORK_DENYLIST = {"agents", "langchain", "llama_index"}


@pytest.mark.asyncio
async def test_add_memory_uses_default_user_id(monkeypatch):
    mock_add = AsyncMock(return_value=None)
    monkeypatch.setattr(mem0_core.client, "add", mock_add)

    result = await mem0_core.add_memory("I prefer dark mode")

    mock_add.assert_awaited_once_with(
        [{"role": "user", "content": "I prefer dark mode"}],
        user_id=mem0_core.DEFAULT_USER_ID,
    )
    assert result == "Stored message: I prefer dark mode"


@pytest.mark.asyncio
async def test_add_memory_uses_explicit_user_id(monkeypatch):
    mock_add = AsyncMock(return_value=None)
    monkeypatch.setattr(mem0_core.client, "add", mock_add)

    result = await mem0_core.add_memory("I prefer dark mode", user_id="ish")

    mock_add.assert_awaited_once_with(
        [{"role": "user", "content": "I prefer dark mode"}],
        user_id="ish",
    )
    assert result == "Stored message: I prefer dark mode"


@pytest.mark.asyncio
async def test_search_memory_uses_default_user_id(monkeypatch):
    mock_search = AsyncMock(
        return_value={"results": [{"memory": "likes dark mode"}, {"memory": "uses vim"}]}
    )
    monkeypatch.setattr(mem0_core.client, "search", mock_search)

    result = await mem0_core.search_memory("ui preferences")

    mock_search.assert_awaited_once_with(
        "ui preferences", filters={"user_id": mem0_core.DEFAULT_USER_ID}
    )
    assert result == "likes dark mode\nuses vim"


@pytest.mark.asyncio
async def test_search_memory_uses_explicit_user_id(monkeypatch):
    mock_search = AsyncMock(return_value={"results": [{"memory": "likes dark mode"}]})
    monkeypatch.setattr(mem0_core.client, "search", mock_search)

    result = await mem0_core.search_memory("ui preferences", user_id="ish")

    mock_search.assert_awaited_once_with("ui preferences", filters={"user_id": "ish"})
    assert result == "likes dark mode"


@pytest.mark.asyncio
async def test_get_all_memory_uses_default_user_id(monkeypatch):
    mock_get_all = AsyncMock(
        return_value={"results": [{"memory": "likes dark mode"}, {"memory": "uses vim"}]}
    )
    monkeypatch.setattr(mem0_core.client, "get_all", mock_get_all)

    result = await mem0_core.get_all_memory()

    mock_get_all.assert_awaited_once_with(filters={"user_id": mem0_core.DEFAULT_USER_ID})
    assert result == "likes dark mode\nuses vim"


@pytest.mark.asyncio
async def test_get_all_memory_uses_explicit_user_id(monkeypatch):
    mock_get_all = AsyncMock(return_value={"results": [{"memory": "likes dark mode"}]})
    monkeypatch.setattr(mem0_core.client, "get_all", mock_get_all)

    result = await mem0_core.get_all_memory(user_id="ish")

    mock_get_all.assert_awaited_once_with(filters={"user_id": "ish"})
    assert result == "likes dark mode"


def test_core_has_no_agent_framework_imports():
    """PRD §5 invariant 3: mem0_core.py must not import any agent framework.

    Parses the AST directly rather than inspecting sys.modules, so the
    result is deterministic and independent of what else the test
    session happens to have imported.
    """
    source = Path(mem0_core.__file__).read_text()
    tree = ast.parse(source)

    imported_roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_roots.add(node.module.split(".")[0])

    forbidden = imported_roots & AGENT_FRAMEWORK_DENYLIST
    assert not forbidden, f"mem0_core.py imports agent-framework package(s): {forbidden}"
