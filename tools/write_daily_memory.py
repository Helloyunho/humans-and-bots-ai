from typing import TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from main import HumansAndBotsAI


async def callback(_: "HumansAndBotsAI", memory: str) -> str:
    date = datetime.now().strftime("%Y-%m-%d")
    memory_path = f"memory/{date}.md"

    with open(memory_path, "a") as f:
        f.write(memory + "\n")
    return memory
