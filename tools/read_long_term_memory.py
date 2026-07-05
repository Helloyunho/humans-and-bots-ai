from typing import TYPE_CHECKING
import os

if TYPE_CHECKING:
    from main import HumansAndBotsAI


async def callback(_: "HumansAndBotsAI") -> str:
    memory_path = f"memory/LONG_TERM_MEMORY.md"

    if not os.path.exists(memory_path):
        with open(memory_path, "w") as f:
            f.write(f"# Long Term Memory\n\n")
    with open(memory_path, "r") as f:
        memory_content = f.read()
    return memory_content
