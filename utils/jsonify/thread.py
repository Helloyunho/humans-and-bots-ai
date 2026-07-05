from discord import Thread


def jsonify_thread(thread: Thread) -> dict:
    return {
        "id": str(thread.id),
        "name": thread.name,
        "type": str(thread.type),
        "archived": thread.archived,
        "archive_timestamp": thread.archive_timestamp.isoformat(),
        "auto_archive_duration": thread.auto_archive_duration,
        "category_id": str(thread.category_id) if thread.category_id else None,
        "created_at": thread.created_at.isoformat() if thread.created_at else None,
        "last_message_id": (
            str(thread.last_message_id) if thread.last_message_id else None
        ),
        "owner_id": str(thread.owner_id) if thread.owner_id else None,
        "parent_id": str(thread.parent_id) if thread.parent_id else None,
        "member_count": thread.member_count,
        "slowmode_delay": thread.slowmode_delay,
        "starter_message_id": (
            str(thread.starter_message.id) if thread.starter_message else None
        ),
    }
