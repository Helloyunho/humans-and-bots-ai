from discord import Member
from .role import jsonify_role


def jsonify_member(member: Member) -> dict:
    return {
        "id": str(member.id),
        "name": member.name,
        "discriminator": member.discriminator,
        "avatar": str(member.avatar.url) if member.avatar else None,
        "bot": member.bot,
        "joined_at": member.joined_at.isoformat() if member.joined_at else None,
        "roles": [jsonify_role(role) for role in member.roles],
        "nick": member.nick,
        "premium_since": (
            member.premium_since.isoformat() if member.premium_since else None
        ),
        "guild_permissions": str(member.guild_permissions),
    }
