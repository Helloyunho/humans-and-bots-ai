from typing import TYPE_CHECKING
import json
from discord import TextChannel, Thread
from utils.jsonify.text_channel import jsonify_text_channel
from utils.jsonify.thread import jsonify_thread

if TYPE_CHECKING:
    from main import HumansAndBotsAI


async def callback(bot: "HumansAndBotsAI") -> str:
    guild_id = 1523270943827300474
    guild = bot.get_guild(guild_id)
    if guild is None:
        return f"Guild with ID {guild_id} not found."

    channels = []
    for channel in guild.channels:
        channels.append(
            jsonify_thread(channel)
            if isinstance(channel, Thread)
            else (
                jsonify_text_channel(channel)
                if isinstance(channel, TextChannel)
                else {"id": str(channel.id), "name": channel.name}
            )
        )

    return json.dumps(channels, indent=4)
