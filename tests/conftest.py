from __future__ import annotations

from unittest.mock import MagicMock, patch

# mem0_core.py constructs AsyncMemoryClient at import time, and that
# constructor validates the API key against the live host. Patch the
# class before the first import so no test run ever touches the network.
with patch("mem0.AsyncMemoryClient") as _MockAsyncMemoryClient:
    _MockAsyncMemoryClient.return_value = MagicMock()
    import mem0_core  # noqa: F401
