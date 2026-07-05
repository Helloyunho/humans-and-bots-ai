from discord import TextChannel


def jsonify_text_channel(channel: TextChannel) -> dict:
    return {
        "id": str(channel.id),
        "name": channel.name,
        "type": str(channel.type),
        "position": channel.position,
        "topic": channel.topic,
        "nsfw": channel.nsfw,
        "slowmode_delay": channel.slowmode_delay,
        "category_id": str(channel.category_id) if channel.category_id else None,
        "last_message_id": (
            str(channel.last_message_id) if channel.last_message_id else None
        ),
        "created_at": channel.created_at.isoformat() if channel.created_at else None,
        # threads
    }
