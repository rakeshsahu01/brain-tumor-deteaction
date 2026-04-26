from datetime import datetime


def serialize_record(record):
    if not record:
        return None
    serialized = {
        "id": str(record.get("_id")),
        "patient": record.get("patient", {}),
        "prediction": record.get("prediction", {}),
        "createdAt": record.get("createdAt"),
        "images": record.get("images", {}),
    }
    created_at = serialized["createdAt"]
    if isinstance(created_at, datetime):
        serialized["createdAt"] = created_at.isoformat()
    return serialized
