from typing import TYPE_CHECKING
import json
from utils.jsonify.emoji import jsonify_emoji

if TYPE_CHECKING:
    from main import HumansAndBotsAI


async def callback(bot: "HumansAndBotsAI") -> str:
    guild_id = 1523270943827300474
    guild = bot.get_guild(guild_id)
    if guild is None:
        return f"Guild with ID {guild_id} not found."

    emojis = [jsonify_emoji(emoji) for emoji in guild.emojis]

    return json.dumps(emojis, indent=4)
