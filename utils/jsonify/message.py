from discord import Message, Member

from .attachment import jsonify_attachment
from .user import jsonify_user
from .member import jsonify_member
from .reaction import jsonify_reaction
from .embed import jsonify_embed
from .sticker_item import jsonify_sticker_item
from .component import jsonify_component


def jsonify_message(message: Message) -> dict:
    return {
        "id": str(message.id),
        "author": (
            jsonify_member(message.author)
            if isinstance(message.author, Member)
            else jsonify_user(message.author)
        ),
        "content": message.content,
        "timestamp": message.created_at.isoformat(),
        "attachments": [
            jsonify_attachment(attachment) for attachment in message.attachments
        ],
        "reactions": [jsonify_reaction(reaction) for reaction in message.reactions],
        "channel_id": str(message.channel.id),
        "embeds": [jsonify_embed(embed) for embed in message.embeds],
        "mentions": {
            "users": [user.id for user in message.mentions],
            "roles": [role.id for role in message.role_mentions],
            "channels": [channel.id for channel in message.channel_mentions],
        },
        "pinned": message.pinned,
        "pinned_at": message.pinned_at.isoformat() if message.pinned_at else None,
        "edited_at": message.edited_at.isoformat() if message.edited_at else None,
        "type": str(message.type),
        "reference": {
            "channel_id": (
                str(message.reference.channel_id)
                if message.reference and message.reference.channel_id
                else None
            ),
            "message_id": (
                str(message.reference.message_id)
                if message.reference and message.reference.message_id
                else None
            ),
        },
        "stickers": [jsonify_sticker_item(sticker) for sticker in message.stickers],
        "components": [
            jsonify_component(component) for component in message.components
        ],
    }
