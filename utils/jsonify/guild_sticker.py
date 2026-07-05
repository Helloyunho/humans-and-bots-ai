from discord import GuildSticker


def jsonify_guild_sticker(sticker: GuildSticker) -> dict:
    return {
        "id": str(sticker.id),
        "name": sticker.name,
        "description": sticker.description,
        "type": str(sticker.type),
        "format": str(sticker.format),
        "available": sticker.available,
        "user_id": str(sticker.user.id) if sticker.user else None,
    }
