from datetime import datetime

from flask import jsonify, request
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash

from backend.models.db import users_collection


def signup():
    payload = request.get_json() or {}
    name = payload.get("name", "").strip()
    email = payload.get("email", "").strip().lower()
    password = payload.get("password", "").strip()

    if not name or not email or not password:
        return jsonify({"message": "Name, email and password are required"}), 400

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


def login():
    payload = request.get_json() or {}
    email = payload.get("email", "").strip().lower()
    password = payload.get("password", "").strip()

    user = users_collection.find_one({"email": email})
    if not user or not check_password_hash(user.get("passwordHash", ""), password):
        return jsonify({"message": "Invalid email or password"}), 401

    token = create_access_token(identity=email)
    return jsonify({"token": token, "user": {"name": user.get("name"), "email": email}}), 200
