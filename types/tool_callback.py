from typing import TYPE_CHECKING, Protocol, Any

if TYPE_CHECKING:
    from main import HumansAndBotsAI


class ToolCallback(Protocol):
    async def __call__(
        self, bot: "HumansAndBotsAI", *args: Any, **kwargs: Any
    ) -> str: ...
