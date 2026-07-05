from discord import Emoji


def jsonify_emoji(emoji: Emoji) -> dict:
    return {
        "id": str(emoji.id),
        "name": emoji.name,
        "animated": emoji.animated,
        "available": emoji.available,
        "url": str(emoji.url),
    }
