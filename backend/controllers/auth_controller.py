from datetime import datetime

from flask import jsonify, request
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash

from backend.models.db import get_users_collection


def signup():
    payload = request.get_json() or {}
    name = payload.get("name", "").strip()
    email = payload.get("email", "").strip().lower()
    password = payload.get("password", "").strip()

    if not name or not email or not password:
        return jsonify({"message": "Name, email and password are required"}), 400

    try:
        users_collection = get_users_collection()
        if not users_collection:
            return jsonify({"message": "Database temporarily unavailable"}), 503
        
        if users_collection.find_one({"email": email}):
            return jsonify({"message": "User already exists"}), 409

        users_collection.insert_one(
            {
                "name": name,
                "email": email,
                "passwordHash": generate_password_hash(password),
                "createdAt": datetime.utcnow(),
            }
        )

        token = create_access_token(identity=email)
        return jsonify({"token": token, "user": {"name": name, "email": email}}), 201
    except Exception as e:
        return jsonify({"message": f"Signup failed: {str(e)}"}), 500


def login():
    payload = request.get_json() or {}
    email = payload.get("email", "").strip().lower()
    password = payload.get("password", "").strip()

    try:
        users_collection = get_users_collection()
        if not users_collection:
            return jsonify({"message": "Database temporarily unavailable"}), 503
        
        user = users_collection.find_one({"email": email})
        if not user or not check_password_hash(user.get("passwordHash", ""), password):
            return jsonify({"message": "Invalid email or password"}), 401

        token = create_access_token(identity=email)
        return jsonify({"token": token, "user": {"name": user.get("name"), "email": email}}), 200
    except Exception as e:
        return jsonify({"message": f"Login failed: {str(e)}"}), 500
