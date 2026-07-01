import base64
import json
from datetime import datetime
from app.schemas import PaginationCursor


def encode_cursor(cursor: PaginationCursor) -> str:
    payload = {
        "created_at": cursor.created_at.isoformat(),
        "id": cursor.id,
    }

    raw = json.dumps(payload).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("utf-8")


def decode_cursor(cursor_str: str) -> PaginationCursor:
    raw = base64.urlsafe_b64decode(cursor_str.encode("utf-8"))
    data = json.loads(raw.decode("utf-8"))

    return PaginationCursor(
        created_at=datetime.fromisoformat(data["created_at"]),
        id=data["id"],
    )
