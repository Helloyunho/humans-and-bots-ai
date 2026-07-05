from discord import Attachment


def jsonify_attachment(attachment: Attachment) -> dict:
    return {
        "id": str(attachment.id),
        "filename": attachment.filename,
        "url": attachment.url,
        "size": attachment.size,
        "content_type": attachment.content_type,
    }
