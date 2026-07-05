from discord import User


def jsonify_user(user: User) -> dict:
    return {
        "id": str(user.id),
        "name": user.name,
        "discriminator": user.discriminator,
        "avatar": str(user.avatar.url) if user.avatar else None,
        "bot": user.bot,
    }
