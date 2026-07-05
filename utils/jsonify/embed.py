from discord import Embed


def jsonify_embed(embed: Embed) -> dict:
    return {
        "title": embed.title,
        "type": embed.type,
        "description": embed.description,
        "url": embed.url,
        "color": embed.color.value if embed.color else None,
        "timestamp": embed.timestamp.isoformat() if embed.timestamp else None,
        "footer": {
            "text": embed.footer.text if embed.footer else None,
            "icon_url": (
                str(embed.footer.icon_url)
                if embed.footer and embed.footer.icon_url
                else None
            ),
        },
        "image": {
            "url": str(embed.image.url) if embed.image else None,
        },
        "thumbnail": {
            "url": str(embed.thumbnail.url) if embed.thumbnail else None,
        },
        "video": {
            "url": str(embed.video.url) if embed.video else None,
        },
        "provider": {
            "name": embed.provider.name if embed.provider else None,
            "url": (
                str(embed.provider.url)
                if embed.provider and embed.provider.url
                else None
            ),
        },
        "author": {
            "name": embed.author.name if embed.author else None,
            "url": str(embed.author.url) if embed.author and embed.author.url else None,
            "icon_url": (
                str(embed.author.icon_url)
                if embed.author and embed.author.icon_url
                else None
            ),
        },
        "fields": [
            {
                "name": field.name,
                "value": field.value,
                "inline": field.inline,
            }
            for field in embed.fields
        ],
        "flags": embed.flags.value,
    }
