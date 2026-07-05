from discord import Sticker, StickerItem


def jsonify_sticker_item(sticker: StickerItem) -> dict:
    return {
        "id": str(sticker.id),
        "name": sticker.name,
        "format": str(sticker.format),
        "url": sticker.url,
    }
