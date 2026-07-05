from typing import TYPE_CHECKING
from discord import TextChannel
import json
from utils.jsonify.message import jsonify_message

if TYPE_CHECKING:
    from main import HumansAndBotsAI


async def callback(bot: "HumansAndBotsAI", channel_id: str, message_id: str) -> str:
    guild_id = 1523270943827300474
    guild = bot.get_guild(guild_id)
    if guild is None:
        return f"Guild with ID {guild_id} not found."

    channel = guild.get_channel(int(channel_id))
    if channel is None:
        return f"Channel with ID {channel_id} not found."
    if not isinstance(channel, TextChannel):
        return f"Channel with ID {channel_id} is not a text channel."

    msg = await channel.fetch_message(int(message_id))
    return json.dumps(jsonify_message(msg), indent=4)
