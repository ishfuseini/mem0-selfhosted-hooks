from __future__ import annotations

import os

from dotenv import load_dotenv

try:
    from mem0 import AsyncMemoryClient
except ImportError:
    raise ImportError("mem0 is not installed. Please install it using 'pip install mem0ai'.")

load_dotenv()

client = AsyncMemoryClient(api_key=os.getenv("MEM0_API_KEY"), host=os.getenv("MEM0_HOST"))

DEFAULT_USER_ID = "default_user"


async def add_memory(content: str, user_id: str | None = None) -> str:
    """Store a message in Mem0 for the given user."""
    messages = [{"role": "user", "content": content}]
    await client.add(messages, user_id=user_id or DEFAULT_USER_ID)
    return f"Stored message: {content}"


async def search_memory(query: str, user_id: str | None = None) -> str:
    """Search a user's memories in Mem0 and return matching memory text, one per line."""
    memories = await client.search(query, filters={"user_id": user_id or DEFAULT_USER_ID})
    return "\n".join(result["memory"] for result in memories["results"])


async def get_all_memory(user_id: str | None = None) -> str:
    """Retrieve all of a user's memories from Mem0, one per line."""
    memories = await client.get_all(filters={"user_id": user_id or DEFAULT_USER_ID})
    return "\n".join(result["memory"] for result in memories["results"])
