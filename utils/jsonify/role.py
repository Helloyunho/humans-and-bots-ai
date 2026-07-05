from discord import Role


def jsonify_role(role: Role) -> dict:
    return {
        "id": str(role.id),
        "name": role.name,
        "color": role.color.value,
        "hoist": role.hoist,
        "position": role.position,
        "permissions": str(role.permissions),
        "managed": role.managed,
        "mentionable": role.mentionable,
        "icon": str(role.icon.url) if role.icon else None,
        "unicode_emoji": role.unicode_emoji,
        # members
    }
