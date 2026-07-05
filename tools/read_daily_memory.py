from typing import TYPE_CHECKING
from datetime import datetime
import os

if TYPE_CHECKING:
    from main import HumansAndBotsAI


async def callback(_: "HumansAndBotsAI") -> str:
    date = datetime.now().strftime("%Y-%m-%d")
    memory_path = f"memory/{date}.md"

    if not os.path.exists(memory_path):
        with open(memory_path, "w") as f:
            f.write(f"# Daily Memory for {date}\n\n")
    with open(memory_path, "r") as f:
        memory_content = f.read()
    return memory_content
