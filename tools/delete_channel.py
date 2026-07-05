from typing import TYPE_CHECKING
from discord import TextChannel, Thread
import json
from utils.jsonify.thread import jsonify_thread
from utils.jsonify.text_channel import jsonify_text_channel

if TYPE_CHECKING:
    from main import HumansAndBotsAI


async def callback(bot: "HumansAndBotsAI", channel_id: str) -> str:
    guild_id = 1523270943827300474
    guild = bot.get_guild(guild_id)
    if guild is None:
        return f"Guild with ID {guild_id} not found."

    channel = guild.get_channel(int(channel_id))
    if channel is None:
        return f"Channel with ID {channel_id} not found."
    await channel.delete()

    return json.dumps(
        (
            jsonify_thread(channel)
            if isinstance(channel, Thread)
            else (
                jsonify_text_channel(channel)
                if isinstance(channel, TextChannel)
                else {
                    "id": str(channel.id),
                    "name": channel.name,
                    "type": str(channel.type),
                }
            )
        ),
        indent=4,
    )
