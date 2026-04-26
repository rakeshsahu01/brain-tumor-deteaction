from datetime import datetime
from random import randint

from bson import ObjectId
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity

from backend.models.db import patients_collection


def _generate_patient_id():
    return f"PT-{datetime.utcnow().strftime('%Y%m%d')}-{randint(1000, 9999)}"


def create_patient():
    payload = request.get_json() or {}
    required_fields = ["fullName", "age", "gender", "phone", "email", "address", "doctorName", "symptoms"]
    missing = [field for field in required_fields if not str(payload.get(field, "")).strip()]
    if missing:
        return jsonify({"message": f"Missing required fields: {', '.join(missing)}"}), 400

    patient_record = {
        "userEmail": get_jwt_identity(),
        "patientId": payload.get("patientId") or _generate_patient_id(),
        "fullName": payload.get("fullName", "").strip(),
        "age": payload.get("age", "").strip(),
        "gender": payload.get("gender", "").strip(),
        "phone": payload.get("phone", "").strip(),
        "email": payload.get("email", "").strip(),
        "address": payload.get("address", "").strip(),
        "doctorName": payload.get("doctorName", "").strip(),
        "allergies": payload.get("allergies", "").strip(),
        "medicalHistory": payload.get("medicalHistory", "").strip(),
        "symptoms": payload.get("symptoms", "").strip(),
        "bloodGroup": payload.get("bloodGroup", "").strip(),
        "createdAt": datetime.utcnow(),
    }
    inserted = patients_collection.insert_one(patient_record)
    saved = patients_collection.find_one({"_id": inserted.inserted_id})
    return (
        jsonify(
            {
                "patient": {
                    "id": str(saved["_id"]),
                    "patientId": saved["patientId"],
                    "fullName": saved["fullName"],
                    "age": saved["age"],
                    "gender": saved["gender"],
                    "phone": saved["phone"],
                    "email": saved["email"],
                    "address": saved["address"],
                    "doctorName": saved["doctorName"],
                    "allergies": saved["allergies"],
                    "medicalHistory": saved["medicalHistory"],
                    "symptoms": saved["symptoms"],
                    "bloodGroup": saved["bloodGroup"],
                }
            }
        ),
        201,
    )


def get_patient(patient_id):
    email = get_jwt_identity()
    try:
        record = patients_collection.find_one({"_id": ObjectId(patient_id), "userEmail": email})
    except Exception:
        record = None
    if not record:
        return jsonify({"message": "Patient not found"}), 404
    return (
        jsonify(
            {
                "patient": {
                    "id": str(record["_id"]),
                    "patientId": record["patientId"],
                    "fullName": record["fullName"],
                    "age": record["age"],
                    "gender": record["gender"],
                    "phone": record["phone"],
                    "email": record["email"],
                    "address": record["address"],
                    "doctorName": record["doctorName"],
                    "allergies": record["allergies"],
                    "medicalHistory": record["medicalHistory"],
                    "symptoms": record["symptoms"],
                    "bloodGroup": record["bloodGroup"],
                }
            }
        ),
        200,
    )
