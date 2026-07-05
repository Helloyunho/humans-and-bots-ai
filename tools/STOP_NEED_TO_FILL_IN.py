from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import HumansAndBotsAI


async def callback(_: "HumansAndBotsAI") -> str:
    # user didn't fill in the information yet, so we stop the process and ask them to fill it in
    print("Please fill in the information in md/PERSONA.md before proceeding.")
    exit(1)
