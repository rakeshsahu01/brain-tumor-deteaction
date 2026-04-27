from flask import jsonify
from flask_jwt_extended import get_jwt_identity

from backend.models.db import get_history_collection
from backend.utils.serialize import serialize_record


def get_history():
    try:
        email = get_jwt_identity()
        history_collection = get_history_collection()
        if not history_collection:
            return jsonify({"records": [], "warning": "History database temporarily unavailable"}), 200
        
        records = history_collection.find({"userEmail": email}).sort("createdAt", -1)
        return jsonify({"records": [serialize_record(item) for item in records]}), 200
    except Exception as e:
        return jsonify({"records": [], "warning": f"Failed to retrieve history: {str(e)}"}), 200
