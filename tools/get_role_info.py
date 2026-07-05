from typing import TYPE_CHECKING
import json
from utils.jsonify.member import jsonify_member
from utils.jsonify.role import jsonify_role

if TYPE_CHECKING:
    from main import HumansAndBotsAI


async def callback(bot: "HumansAndBotsAI", role_id: str) -> str:
    guild_id = 1523270943827300474
    guild = bot.get_guild(guild_id)
    if guild is None:
        return f"Guild with ID {guild_id} not found."

    role = guild.get_role(int(role_id))
    if role is None:
        return f"Role with ID {role_id} not found."

    members = [jsonify_member(member) for member in role.members]
    role = jsonify_role(role)
    role["members"] = members

    return json.dumps(role, indent=4)
