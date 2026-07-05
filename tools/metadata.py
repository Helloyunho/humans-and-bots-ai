from typing import TypedDict, Literal, NotRequired


class Property(TypedDict):
    type: (
        Literal["string", "number", "boolean", "object", "array", "null"]
        | list[Literal["string", "number", "boolean", "object", "array", "null"]]
    )
    enum: NotRequired[list[str] | None]
    default: NotRequired[str | None]
    examples: NotRequired[list[str] | None]
    description: NotRequired[str | None]


class Parameters(TypedDict):
    type: Literal["object"]
    properties: dict[str, Property]
    required: NotRequired[list[str] | None]


class FunctionTool(TypedDict):
    name: str
    parameters: NotRequired[Parameters | None]
    strict: NotRequired[bool | None]
    type: Literal["function"]
    defer_loading: NotRequired[bool | None]
    description: NotRequired[str | None]


TOOL_LIST: list[FunctionTool] = [
    {
        "type": "function",
        "name": "STOP_NEED_TO_FILL_IN",
        "description": "Stops the bot immediately and notify user to fill in the missing information in the PERSONA.md file.",
        "strict": True,
    },
    {
        "type": "function",
        "name": "read_daily_memory",
        "description": "Reads the daily memory for today.",
        "strict": True,
    },
    {
        "type": "function",
        "name": "write_daily_memory",
        "description": "Writes(appends) the daily memory for today.",
        "parameters": {
            "type": "object",
            "properties": {
                "memory": {
                    "type": "string",
                    "description": "The memory to write for today.",
                }
            },
            "required": ["memory"],
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "read_long_term_memory",
        "description": "Reads the long term memory.",
        "strict": True,
    },
    {
        "type": "function",
        "name": "write_long_term_memory",
        "description": "Writes(appends) the long term memory.",
        "parameters": {
            "type": "object",
            "properties": {
                "memory": {
                    "type": "string",
                    "description": "The memory to write for long term memory.",
                }
            },
            "required": ["memory"],
        },
        "strict": True,
    },
    # necessary discord api functions
    {
        "type": "function",
        "name": "get_guild_channels",
        "description": "Gets all the channels in the guild. Response will be a JSON array of partial channel(id, name, type) objects.",
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_channel_messages",
        "description": "Gets the last 50 messages in a channel. Response will be a JSON array of message objects.",
        "parameters": {
            "type": "object",
            "properties": {
                "channel_id": {
                    "type": "string",
                    "description": "The ID of the channel to get messages from.",
                }
            },
            "required": ["channel_id"],
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "send_message",
        "description": "Sends a message to a channel. Response will be a JSON object of the sent message.",
        "parameters": {
            "type": "object",
            "properties": {
                "channel_id": {
                    "type": "string",
                    "description": "The ID of the channel to send the message to.",
                },
                "message": {
                    "type": "string",
                    "description": "The message content to send.",
                },
            },
            "required": ["channel_id", "message"],
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "edit_message",
        "description": "Edits a message in a channel. Response will be a JSON object of the edited message.",
        "parameters": {
            "type": "object",
            "properties": {
                "channel_id": {
                    "type": "string",
                    "description": "The ID of the channel to edit the message in.",
                },
                "message_id": {
                    "type": "string",
                    "description": "The ID of the message to edit.",
                },
                "new_message": {
                    "type": "string",
                    "description": "The new message content.",
                },
            },
            "required": ["channel_id", "message_id", "new_message"],
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "delete_message",
        "description": "Deletes a message in a channel. Response will be a JSON object of the deleted message.",
        "parameters": {
            "type": "object",
            "properties": {
                "channel_id": {
                    "type": "string",
                    "description": "The ID of the channel to delete the message from.",
                },
                "message_id": {
                    "type": "string",
                    "description": "The ID of the message to delete.",
                },
            },
            "required": ["channel_id", "message_id"],
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "react_to_message",
        "description": "Adds a reaction to a message in a channel. Responds 'OK' if the reaction is added successfully.",
        "parameters": {
            "type": "object",
            "properties": {
                "channel_id": {
                    "type": "string",
                    "description": "The ID of the channel to add the reaction in.",
                },
                "message_id": {
                    "type": "string",
                    "description": "The ID of the message to add the reaction to.",
                },
                "emoji": {
                    "type": "string",
                    "description": "The emoji to add as a reaction.",
                },
            },
            "required": ["channel_id", "message_id", "emoji"],
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "send_typing_indicator",
        "description": "Sends a typing indicator to a channel. Response will be 'OK' if the typing indicator is sent successfully.",
        "parameters": {
            "type": "object",
            "properties": {
                "channel_id": {
                    "type": "string",
                    "description": "The ID of the channel to send the typing indicator to.",
                }
            },
            "required": ["channel_id"],
        },
        "strict": True,
    },
    # not that necessary discord api functions
    {
        "type": "function",
        "name": "get_channel_info",
        "description": "Gets the information of a channel. Response will be a JSON object of the channel.",
        "parameters": {
            "type": "object",
            "properties": {
                "channel_id": {
                    "type": "string",
                    "description": "The ID of the channel to get information from.",
                }
            },
            "required": ["channel_id"],
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_message_info",
        "description": "Gets the information of a message. Response will be a JSON object of the message.",
        "parameters": {
            "type": "object",
            "properties": {
                "channel_id": {
                    "type": "string",
                    "description": "The ID of the channel to get information from.",
                },
                "message_id": {
                    "type": "string",
                    "description": "The ID of the message to get information from.",
                },
            },
            "required": ["channel_id", "message_id"],
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_user_info",
        "description": "Gets the information of a user. Response will be a JSON object of the user.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The ID of the user to get information from.",
                }
            },
            "required": ["user_id"],
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_guild_info",
        "description": "Gets the information of a guild. Response will be a JSON object of the guild.",
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_guild_members",
        "description": "Gets the members of a guild. Response will be a JSON array of member objects.",
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_guild_roles",
        "description": "Gets the roles of a guild. Response will be a JSON array of role objects.",
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_guild_emojis",
        "description": "Gets the emojis of a guild. Response will be a JSON array of emoji objects.",
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_guild_stickers",
        "description": "Gets the stickers of a guild. Response will be a JSON array of sticker objects.",
        "strict": True,
    },
    {
        "type": "function",
        "name": "change_nickname",
        "description": "Changes the nickname of a user in a guild. Response will be a JSON object of the user.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The ID of the user to change the nickname of.",
                },
                "new_nickname": {
                    "type": ["string", "null"],
                    "description": "The new nickname to set for the user. If null, the nickname will be reset to the default username.",
                },
            },
            "required": ["user_id", "new_nickname"],
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "create_thread",
        "description": "Creates a thread in a channel. Response will be a JSON object of the created thread.",
        "parameters": {
            "type": "object",
            "properties": {
                "channel_id": {
                    "type": "string",
                    "description": "The ID of the channel to create the thread in.",
                },
                "thread_name": {
                    "type": "string",
                    "description": "The name of the thread to create.",
                },
                "message_id": {
                    "type": ["string", "null"],
                    "description": "The ID of the message to start the thread with. If null, the thread will be created without a starting message(private).",
                },
            },
            "required": ["channel_id", "thread_name", "message_id"],
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_role_info",
        "description": "Gets information about a specific role in the guild. Response will be a JSON object of the role.",
        "parameters": {
            "type": "object",
            "properties": {
                "role_id": {
                    "type": "string",
                    "description": "The ID of the role to get information about.",
                }
            },
            "required": ["role_id"],
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_me",
        "description": "Gets information about the bot itself. Response will be a JSON object of the bot user.",
        "strict": True,
    },
    # moderation functions
    {
        "type": "function",
        "name": "ban_user",
        "description": "Bans a user from the guild. Response will be a JSON object of the user.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The ID of the user to ban.",
                },
                "reason": {
                    "type": ["string", "null"],
                    "description": "The reason for the ban. If null, no reason will be provided.",
                },
            },
            "required": ["user_id", "reason"],
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "kick_user",
        "description": "Kicks a user from the guild. Response will be a JSON object of the user.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The ID of the user to kick.",
                },
                "reason": {
                    "type": ["string", "null"],
                    "description": "The reason for the kick. If null, no reason will be provided.",
                },
            },
            "required": ["user_id", "reason"],
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "timeout_user",
        "description": "Timeouts a user in the guild. Response will be a JSON object of the user.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The ID of the user to timeout.",
                },
                "until": {
                    "type": "number",
                    "description": "The timestamp (in milliseconds) until which the user will be timed out.",
                },
                "reason": {
                    "type": ["string", "null"],
                    "description": "The reason for the timeout. If null, no reason will be provided.",
                },
            },
            "required": ["user_id", "until", "reason"],
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "pin_message",
        "description": "Pins a message in a channel. Response will be a JSON object of the message.",
        "parameters": {
            "type": "object",
            "properties": {
                "channel_id": {
                    "type": "string",
                    "description": "The ID of the channel to pin the message in.",
                },
                "message_id": {
                    "type": "string",
                    "description": "The ID of the message to pin.",
                },
            },
            "required": ["channel_id", "message_id"],
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "unpin_message",
        "description": "Unpins a message in a channel. Response will be a JSON object of the message.",
        "parameters": {
            "type": "object",
            "properties": {
                "channel_id": {
                    "type": "string",
                    "description": "The ID of the channel to unpin the message in.",
                },
                "message_id": {
                    "type": "string",
                    "description": "The ID of the message to unpin.",
                },
            },
            "required": ["channel_id", "message_id"],
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "delete_channel",
        "description": "Deletes a channel in the guild. This was intended for thread deletion. Response will be a JSON object of the deleted channel.",
        "parameters": {
            "type": "object",
            "properties": {
                "channel_id": {
                    "type": "string",
                    "description": "The ID of the channel to delete.",
                }
            },
            "required": ["channel_id"],
        },
        "strict": True,
    },
]
