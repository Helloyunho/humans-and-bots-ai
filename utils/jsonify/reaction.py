from discord import Reaction


def jsonify_reaction(reaction: Reaction) -> dict:
    return {
        "emoji": str(reaction.emoji),
        "count": reaction.count,
        "me": reaction.me,
        "message_id": str(reaction.message.id),
    }
