from datetime import datetime

from bson import ObjectId
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity

from backend.models.db import history_collection, patients_collection
from backend.utils.model_utils import generate_gradcam, predict_image
from backend.utils.serialize import serialize_record


def create_prediction():
    try:
        payload = request.get_json() or {}
        patient = payload.get("patient", {})
        patient_id = payload.get("patientId")
        base64_image = payload.get("image")
        if not base64_image:
            return jsonify({"message": "MRI image is required"}), 400

        user_email = get_jwt_identity()
        if patient_id:
            try:
                patient_doc = patients_collection.find_one({"_id": ObjectId(patient_id), "userEmail": user_email})
            except Exception:
                patient_doc = None
            if not patient_doc:
                return jsonify({"message": "Invalid patient selected"}), 404
            patient = {
                "patientId": patient_doc.get("patientId", ""),
                "fullName": patient_doc.get("fullName", ""),
                "age": patient_doc.get("age", ""),
                "gender": patient_doc.get("gender", ""),
                "phone": patient_doc.get("phone", ""),
                "email": patient_doc.get("email", ""),
                "address": patient_doc.get("address", ""),
                "doctorName": patient_doc.get("doctorName", ""),
                "allergies": patient_doc.get("allergies", ""),
                "medicalHistory": patient_doc.get("medicalHistory", ""),
                "symptoms": patient_doc.get("symptoms", ""),
                "bloodGroup": patient_doc.get("bloodGroup", ""),
            }

        prediction_result = predict_image(base64_image)
        gradcam = generate_gradcam(base64_image)

        record = {
            "userEmail": user_email,
            "patient": {
                "patientId": patient.get("patientId", ""),
                "fullName": patient.get("fullName", ""),
                "age": patient.get("age", ""),
                "gender": patient.get("gender", ""),
                "phone": patient.get("phone", ""),
                "email": patient.get("email", ""),
                "address": patient.get("address", ""),
                "doctorName": patient.get("doctorName", ""),
                "allergies": patient.get("allergies", ""),
                "medicalHistory": patient.get("medicalHistory", ""),
                "symptoms": patient.get("symptoms", ""),
                "bloodGroup": patient.get("bloodGroup", ""),
            },
            "prediction": {
                "predictedClass": prediction_result["predictedClass"],
                "confidence": prediction_result["confidence"],
                "scores": prediction_result["scores"],
            },
            "images": {
                "original": gradcam["originalImage"],
                "heatmap": gradcam["heatmapImage"],
                "overlay": gradcam["overlayImage"],
                "uploaded": base64_image.split(",")[-1],
            },
            "createdAt": datetime.utcnow(),
        }
        inserted = history_collection.insert_one(record)
        stored = history_collection.find_one({"_id": inserted.inserted_id})
        return jsonify({"record": serialize_record(stored)}), 201
    except Exception as error:
        return jsonify({"message": f"Prediction failed: {str(error)}"}), 500


def legacy_predict():
    payload = request.get_json() or {}
    images = payload.get("image", [])
    if not images:
        return jsonify({"result": []}), 200
    predictions = []
    for image in images:
        result = predict_image(image)
        scores = result["scores"]
        confidence = 0
        if "Tumor" in scores:
            confidence = scores["Tumor"] / 100
        elif "No Tumor" in scores:
            confidence = 1 - (scores["No Tumor"] / 100)
        predictions.append(confidence)
    return jsonify({"result": predictions}), 200
