from flask import jsonify
from flask_jwt_extended import get_jwt_identity

from backend.models.db import history_collection
from backend.utils.serialize import serialize_record


def get_history():
    email = get_jwt_identity()
    records = history_collection.find({"userEmail": email}).sort("createdAt", -1)
    return jsonify({"records": [serialize_record(item) for item in records]}), 200
