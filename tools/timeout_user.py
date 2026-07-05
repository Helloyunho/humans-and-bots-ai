from typing import TYPE_CHECKING
import json
from utils.jsonify.member import jsonify_member
from datetime import timedelta

if TYPE_CHECKING:
    from main import HumansAndBotsAI


async def callback(
    bot: "HumansAndBotsAI", user_id: str, until: int, reason: str | None = None
) -> str:
    guild_id = 1523270943827300474
    guild = bot.get_guild(guild_id)
    if guild is None:
        return f"Guild with ID {guild_id} not found."

    member = guild.get_member(int(user_id))
    if member is None:
        return f"Member with ID {user_id} not found."

    await member.timeout(timedelta(milliseconds=until), reason=reason)

    return json.dumps(jsonify_member(member), indent=4)
