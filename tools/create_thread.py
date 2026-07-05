from typing import TYPE_CHECKING
from discord import TextChannel, Object
import json
from utils.jsonify.thread import jsonify_thread

if TYPE_CHECKING:
    from main import HumansAndBotsAI


async def callback(
    bot: "HumansAndBotsAI",
    channel_id: str,
    thread_name: str,
    message_id: str | None = None,
) -> str:
    guild_id = 1523270943827300474
    guild = bot.get_guild(guild_id)
    if guild is None:
        return f"Guild with ID {guild_id} not found."

    channel = guild.get_channel(int(channel_id))
    if channel is None:
        return f"Channel with ID {channel_id} not found."
    if not isinstance(channel, TextChannel):
        return f"Channel with ID {channel_id} is not a text channel."

    thread = await channel.create_thread(
        name=thread_name, message=Object(id=int(message_id)) if message_id else None
    )
    return json.dumps(jsonify_thread(thread), indent=4)
