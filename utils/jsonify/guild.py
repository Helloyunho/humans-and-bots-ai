from discord import Guild


def jsonify_guild(guild: Guild) -> dict:
    return {
        "id": str(guild.id),
        "name": guild.name,
        "owner": str(guild.owner.id) if guild.owner else None,
        "icon": str(guild.icon.url) if guild.icon else None,
        "splash": str(guild.splash.url) if guild.splash else None,
        "banner": str(guild.banner.url) if guild.banner else None,
        "description": guild.description,
        "owner_id": str(guild.owner_id),
        "afk_channel_id": str(guild.afk_channel.id) if guild.afk_channel else None,
        "afk_timeout": guild.afk_timeout,
        "roles": [str(role.id) for role in guild.roles],
        "emojis": [str(emoji.id) for emoji in guild.emojis],
        "features": guild.features,
        "premium_tier": guild.premium_tier,
        "premium_subscription_count": guild.premium_subscription_count,
        "stickers": [str(sticker.id) for sticker in guild.stickers],
        "channels": [str(channel.id) for channel in guild.channels],
    }
