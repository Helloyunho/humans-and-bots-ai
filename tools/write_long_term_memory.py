from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import HumansAndBotsAI


async def callback(_: "HumansAndBotsAI", memory: str) -> str:
    memory_path = f"memory/LONG_TERM_MEMORY.md"

    with open(memory_path, "w") as f:
        f.write(memory + "\n")
    return memory
