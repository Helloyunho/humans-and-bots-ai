import os
from os import getenv
from dotenv import load_dotenv
from utils.openai_client import openai_client, OpenAIStreamingClient
from openai import AsyncOpenAI
import discord
import json
from tools.metadata import TOOL_LIST
from openai.types.chat import ChatCompletionMessage
from typing import TYPE_CHECKING
from datetime import datetime
import importlib
from traceback import print_exc

from utils.jsonify.message import jsonify_message
from utils.jsonify.member import jsonify_member
from utils.jsonify.user import jsonify_user
from utils.jsonify.text_channel import jsonify_text_channel
from utils.jsonify.thread import jsonify_thread
from utils.jsonify.guild import jsonify_guild
from utils.jsonify.role import jsonify_role
from utils.jsonify.emoji import jsonify_emoji
from utils.jsonify.reaction import jsonify_reaction

if TYPE_CHECKING:
    from types.tool_callback import ToolCallback

load_dotenv()

IMPORTED_TOOLS = {}


class HumansAndBotsAI(discord.Client):
    openai_client: AsyncOpenAI
    openai_streaming_client: OpenAIStreamingClient
    model = getenv("OPENAI_MODEL", "gpt-5.4-mini")

    def __init__(self, intents: discord.Intents):
        super().__init__(intents=intents)
        self.openai_client = openai_client
        with open("md/SYSTEM_INSTRUCTION.md", "r") as f:
            self.system_instruction = f.read()
        if not os.path.exists("md/PERSONA.md"):
            raise FileNotFoundError(
                "md/PERSONA.md not found. Perhaps you need to rename md/PERSONA.md.example to md/PERSONA.md and edit it."
            )
        with open("md/PERSONA.md", "r") as f:
            self.persona = f.read()
        self.system_instruction = (
            self.system_instruction.replace("[PERSONA.md]", self.persona)
            .replace("[RULES_CHANNEL_ID]", "1523273541208903690")
            .replace("[BOT_CHANNEL_IDS]", "1523272356154314892, 1523272434776674354")
            .replace("[HUMANS_AND_BOTS_CHANNEL_ID]", "1523272895973822495")
        )
        self.openai_streaming_client = OpenAIStreamingClient(self.openai_client)
        self.openai_streaming_client.on("message", self.on_openai_message)

    async def on_openai_message(self, event: ChatCompletionMessage):
        if event.tool_calls and len(event.tool_calls) > 0:
            tool_output = []
            for tool_call in event.tool_calls:
                call_id = tool_call.id
                name = tool_call.function.name  # type: ignore
                args = json.loads(tool_call.function.arguments)  # type: ignore
                if name not in IMPORTED_TOOLS:
                    IMPORTED_TOOLS[name] = importlib.import_module(
                        f"tools.{name}"
                    ).callback
                tool_callback: ToolCallback = IMPORTED_TOOLS[name]
                try:
                    output = await tool_callback(self, **args)
                except Exception as e:
                    output = str(e)
                    print_exc()
                tool_output.append(
                    {
                        "tool_call_id": call_id,
                        "role": "tool",
                        "content": output,
                    }
                )

            await self.openai_streaming_client.send(
                model=self.model,
                input=tool_output,
                tools=TOOL_LIST,
            )

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")  # type: ignore
        print("------")
        await self.openai_streaming_client.send(
            input=[{"role": "system", "content": self.system_instruction}],
            model=self.model,
            tools=TOOL_LIST,
        )

    async def on_message(self, message: discord.Message):
        if message.author == self.user or message.channel.type in [
            discord.ChannelType.private,
            discord.ChannelType.group,
        ]:
            return
        await self.openai_streaming_client.send(
            model=self.model,
            input=[
                {
                    "role": "user",
                    "content": f"Event: message_created\nData: {json.dumps(jsonify_message(message), indent=4)}",
                }
            ],
            tools=TOOL_LIST,
        )

    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if after.author == self.user or after.channel.type in [
            discord.ChannelType.private,
            discord.ChannelType.group,
        ]:
            return
        await self.openai_streaming_client.send(
            model=self.model,
            input=[
                {
                    "role": "user",
                    "content": f"Event: message_edited\nData: {json.dumps({'before': jsonify_message(before), 'after': jsonify_message(after)}, indent=4)}",
                }
            ],
            tools=TOOL_LIST,
        )

    async def on_message_delete(self, message: discord.Message):
        if message.author == self.user or message.channel.type in [
            discord.ChannelType.private,
            discord.ChannelType.group,
        ]:
            return
        await self.openai_streaming_client.send(
            input=[
                {
                    "role": "user",
                    "content": f"Event: message_deleted\nData: {json.dumps(jsonify_message(message), indent=4)}",
                }
            ],
            model=self.model,
            tools=TOOL_LIST,
        )

    async def on_member_join(self, member: discord.Member):
        await self.openai_streaming_client.send(
            input=[
                {
                    "role": "user",
                    "content": f"Event: member_joined\nData: {json.dumps(jsonify_member(member), indent=4)}",
                }
            ],
            model=self.model,
            tools=TOOL_LIST,
        )

    async def on_member_remove(self, member: discord.Member):
        await self.openai_streaming_client.send(
            input=[
                {
                    "role": "user",
                    "content": f"Event: member_left\nData: {json.dumps(jsonify_member(member), indent=4)}",
                }
            ],
            model=self.model,
            tools=TOOL_LIST,
        )

    async def on_member_update(self, before: discord.Member, after: discord.Member):
        await self.openai_streaming_client.send(
            input=[
                {
                    "role": "user",
                    "content": f"Event: member_updated\nData: {json.dumps({'before': jsonify_member(before), 'after': jsonify_member(after)}, indent=4)}",
                }
            ],
            model=self.model,
            tools=TOOL_LIST,
        )

    async def on_member_ban(self, guild: discord.Guild, user: discord.User):
        await self.openai_streaming_client.send(
            input=[
                {
                    "role": "user",
                    "content": f"Event: member_banned\nData: {json.dumps({'guild': jsonify_guild(guild), 'user': jsonify_user(user)}, indent=4)}",
                }
            ],
            model=self.model,
            tools=TOOL_LIST,
        )

    async def on_guild_update(self, before: discord.Guild, after: discord.Guild):
        await self.openai_streaming_client.send(
            input=[
                {
                    "role": "user",
                    "content": f"Event: guild_updated\nData: {json.dumps({'before': jsonify_guild(before), 'after': jsonify_guild(after)}, indent=4)}",
                }
            ],
            model=self.model,
            tools=TOOL_LIST,
        )

    async def on_guild_emojis_update(
        self,
        guild: discord.Guild,
        before: list[discord.Emoji],
        after: list[discord.Emoji],
    ):
        await self.openai_streaming_client.send(
            input=[
                {
                    "role": "user",
                    "content": f"Event: guild_emojis_updated\nData: {json.dumps({'guild': jsonify_guild(guild), 'before': [jsonify_emoji(e) for e in before], 'after': [jsonify_emoji(e) for e in after]}, indent=4)}",
                }
            ],
            model=self.model,
            tools=TOOL_LIST,
        )

    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):
        await self.openai_streaming_client.send(
            input=[
                {
                    "role": "user",
                    "content": f"Event: guild_channel_created\nData: {json.dumps({'channel': jsonify_thread(channel) if isinstance(channel, discord.Thread) else jsonify_text_channel(channel) if isinstance(channel, discord.TextChannel) else {'id': str(channel.id), 'name': channel.name, 'type': str(channel.type)}}, indent=4)}",
                }
            ],
            model=self.model,
            tools=TOOL_LIST,
        )

    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel):
        await self.openai_streaming_client.send(
            input=[
                {
                    "role": "user",
                    "content": f"Event: guild_channel_deleted\nData: {json.dumps({'channel': jsonify_thread(channel) if isinstance(channel, discord.Thread) else jsonify_text_channel(channel) if isinstance(channel, discord.TextChannel) else {'id': str(channel.id), 'name': channel.name, 'type': str(channel.type)}}, indent=4)}",
                }
            ],
            model=self.model,
            tools=TOOL_LIST,
        )

    async def on_guild_channel_update(
        self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel
    ):
        await self.openai_streaming_client.send(
            input=[
                {
                    "role": "user",
                    "content": f"Event: guild_channel_updated\nData: {json.dumps({'before': jsonify_thread(before) if isinstance(before, discord.Thread) else jsonify_text_channel(before) if isinstance(before, discord.TextChannel) else {'id': str(before.id), 'name': before.name, 'type': str(before.type)}, 'after': jsonify_thread(after) if isinstance(after, discord.Thread) else jsonify_text_channel(after) if isinstance(after, discord.TextChannel) else {'id': str(after.id), 'name': after.name, 'type': str(after.type)}}, indent=4)}",
                }
            ],
            model=self.model,
            tools=TOOL_LIST,
        )

    async def on_guild_channel_pins_update(
        self, channel: discord.abc.GuildChannel, last_pin: datetime | None
    ):
        await self.openai_streaming_client.send(
            input=[
                {
                    "role": "user",
                    "content": f"Event: guild_channel_pins_updated\nData: {json.dumps({'channel': jsonify_thread(channel) if isinstance(channel, discord.Thread) else jsonify_text_channel(channel) if isinstance(channel, discord.TextChannel) else {'id': str(channel.id), 'name': channel.name, 'type': str(channel.type)}, 'last_pin': last_pin if last_pin else None}, indent=4)}",
                }
            ],
            model=self.model,
            tools=TOOL_LIST,
        )

    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        await self.openai_streaming_client.send(
            input=[
                {
                    "role": "user",
                    "content": f"Event: reaction_added\nData: {json.dumps({'reaction': jsonify_reaction(reaction), 'user': jsonify_user(user)}, indent=4)}",
                }
            ],
            model=self.model,
            tools=TOOL_LIST,
        )

    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.User):
        await self.openai_streaming_client.send(
            input=[
                {
                    "role": "user",
                    "content": f"Event: reaction_removed\nData: {json.dumps({'reaction': jsonify_reaction(reaction), 'user': jsonify_user(user)}, indent=4)}",
                }
            ],
            model=self.model,
            tools=TOOL_LIST,
        )

    async def on_reaction_clear(
        self, message: discord.Message, reactions: list[discord.Reaction]
    ):
        await self.openai_streaming_client.send(
            input=[
                {
                    "role": "user",
                    "content": f"Event: reaction_cleared\nData: {json.dumps({'message': jsonify_message(message), 'reactions': [jsonify_reaction(r) for r in reactions]}, indent=4)}",
                }
            ],
            model=self.model,
            tools=TOOL_LIST,
        )

    async def on_reaction_clear_emoji(
        self, message: discord.Message, emoji: discord.PartialEmoji
    ):
        await self.openai_streaming_client.send(
            input=[
                {
                    "role": "user",
                    "content": f"Event: reaction_cleared_emoji\nData: {json.dumps({'message': jsonify_message(message), 'emoji': str(emoji)}, indent=4)}",
                }
            ],
            model=self.model,
            tools=TOOL_LIST,
        )

    async def on_guild_role_create(self, role: discord.Role):
        await self.openai_streaming_client.send(
            input=[
                {
                    "role": "user",
                    "content": f"Event: guild_role_created\nData: {json.dumps({'role': jsonify_role(role)}, indent=4)}",
                }
            ],
            model=self.model,
            tools=TOOL_LIST,
        )

    async def on_guild_role_delete(self, role: discord.Role):
        await self.openai_streaming_client.send(
            input=[
                {
                    "role": "user",
                    "content": f"Event: guild_role_deleted\nData: {json.dumps({'role': jsonify_role(role)}, indent=4)}",
                }
            ],
            model=self.model,
            tools=TOOL_LIST,
        )

    async def on_guild_role_update(self, before: discord.Role, after: discord.Role):
        await self.openai_streaming_client.send(
            input=[
                {
                    "role": "user",
                    "content": f"Event: guild_role_updated\nData: {json.dumps({'before': jsonify_role(before), 'after': jsonify_role(after)}, indent=4)}",
                }
            ],
            model=self.model,
            tools=TOOL_LIST,
        )

    async def on_thread_create(self, thread: discord.Thread):
        await self.openai_streaming_client.send(
            input=[
                {
                    "role": "user",
                    "content": f"Event: thread_created\nData: {json.dumps({'thread': jsonify_thread(thread)}, indent=4)}",
                }
            ],
            model=self.model,
            tools=TOOL_LIST,
        )

    async def on_thread_delete(self, thread: discord.Thread):
        await self.openai_streaming_client.send(
            input=[
                {
                    "role": "user",
                    "content": f"Event: thread_deleted\nData: {json.dumps({'thread': jsonify_thread(thread)}, indent=4)}",
                }
            ],
            model=self.model,
            tools=TOOL_LIST,
        )

    async def on_thread_update(self, before: discord.Thread, after: discord.Thread):
        await self.openai_streaming_client.send(
            input=[
                {
                    "role": "user",
                    "content": f"Event: thread_updated\nData: {json.dumps({'before': jsonify_thread(before), 'after': jsonify_thread(after)}, indent=4)}",
                }
            ],
            model=self.model,
            tools=TOOL_LIST,
        )

    async def on_thread_join(self, thread: discord.Thread):
        await self.openai_streaming_client.send(
            input=[
                {
                    "role": "user",
                    "content": f"Event: thread_joined\nData: {json.dumps({'thread': jsonify_thread(thread)}, indent=4)}",
                }
            ],
            model=self.model,
            tools=TOOL_LIST,
        )

    async def on_thread_remove(self, thread: discord.Thread):
        await self.openai_streaming_client.send(
            input=[
                {
                    "role": "user",
                    "content": f"Event: thread_removed\nData: {json.dumps({'thread': jsonify_thread(thread)}, indent=4)}",
                }
            ],
            model=self.model,
            tools=TOOL_LIST,
        )

    async def on_thread_member_join(self, member: discord.ThreadMember):
        await self.openai_streaming_client.send(
            input=[
                {
                    "role": "user",
                    "content": f"Event: thread_member_joined\nData: {json.dumps({'thread_member': {'id': str(member.id), 'thread': jsonify_thread(member.thread)}}, indent=4)}",
                }
            ],
            model=self.model,
            tools=TOOL_LIST,
        )

    async def on_thread_member_remove(self, member: discord.ThreadMember):
        await self.openai_streaming_client.send(
            input=[
                {
                    "role": "user",
                    "content": f"Event: thread_member_removed\nData: {json.dumps({'thread_member': {'id': str(member.id), 'thread': jsonify_thread(member.thread)}}, indent=4)}",
                }
            ],
            model=self.model,
            tools=TOOL_LIST,
        )


if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    bot = HumansAndBotsAI(intents=intents)
    bot.run(getenv("DISCORD_BOT_TOKEN"))  # type: ignore
