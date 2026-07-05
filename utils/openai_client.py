import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv
from os import getenv

load_dotenv()

openai_client = AsyncOpenAI(
    api_key=getenv("OPENAI_API_KEY"),  # type: ignore
    base_url=getenv("OPENAI_API_BASE_URL"),  # type: ignore
)


class OpenAIStreamingClient:
    def __init__(self, client: AsyncOpenAI):
        self.client = client
        self.chats = []
        self.event_listeners = {}

    async def stream_response(self, model, input, tools):
        resp = await self.client.chat.completions.create(
            model=model,
            messages=input,
            tools=tools,
        )
        if resp.choices[0].message and "message" in self.event_listeners:
            for listener in self.event_listeners["message"]:
                self.chats.append(resp.choices[0].message)
                await listener(resp.choices[0].message)

    async def send(self, model, input, tools):
        self.chats.extend(input)
        if len(self.chats) > 50:
            self.chats = [self.chats[0]] + self.chats[
                -49:
            ]  # Keep only the last 50 messages
        asyncio.create_task(self.stream_response(model, self.chats, tools))

    def on(self, event_type, listener):
        if event_type not in self.event_listeners:
            self.event_listeners[event_type] = []
        self.event_listeners[event_type].append(listener)
