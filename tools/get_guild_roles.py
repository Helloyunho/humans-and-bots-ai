from typing import TYPE_CHECKING
import json
from utils.jsonify.role import jsonify_role

if TYPE_CHECKING:
    from main import HumansAndBotsAI


async def callback(bot: "HumansAndBotsAI") -> str:
    guild_id = 1523270943827300474
    guild = bot.get_guild(guild_id)
    if guild is None:
        return f"Guild with ID {guild_id} not found."

    roles = [jsonify_role(role) for role in guild.roles]

    return json.dumps(roles, indent=4)
