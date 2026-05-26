from datetime import datetime
import logging

from bson import ObjectId
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity

from backend.models.db import get_history_collection, get_patients_collection
from backend.utils.model_utils import generate_gradcam, predict_image
from backend.utils.serialize import serialize_record

logger = logging.getLogger(__name__)


def create_prediction():
    try:
        logger.info("Starting prediction request")
        payload = request.get_json() or {}
        patient = payload.get("patient", {})
        patient_id = payload.get("patientId")
        base64_image = payload.get("image")
        if not base64_image:
            logger.warning("No image provided in prediction request")
            return jsonify({"message": "MRI image is required"}), 400

        user_email = get_jwt_identity()
        if patient_id:
            try:
                # Try to look up in MongoDB if the ID looks like an ObjectId
                patients_collection = get_patients_collection()
                if len(str(patient_id)) == 24 and all(c in '0123456789abcdef' for c in str(patient_id).lower()):
                    patient_doc = patients_collection.find_one({"_id": ObjectId(patient_id), "userEmail": user_email})
                    if patient_doc:
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
            except Exception as e:
                # If MongoDB lookup fails, continue with patient data from payload
                logger.warning(f"Failed to look up patient from MongoDB: {str(e)}")
                pass

        logger.info("Processing image with model")
        prediction_result = predict_image(base64_image)
        logger.info(f"Prediction result: {prediction_result['predictedClass']} ({prediction_result['confidence']}%)")
        
        logger.info("Generating Grad-CAM visualization")
        gradcam = generate_gradcam(base64_image)
        logger.info("Grad-CAM generated successfully")

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
        
        # Try to save to MongoDB if available
        history_collection = get_history_collection()
        if history_collection is not None:
            try:
                inserted = history_collection.insert_one(record)
                stored = history_collection.find_one({"_id": inserted.inserted_id})
                return jsonify({"record": serialize_record(stored)}), 201
            except Exception as mongo_error:
                # If MongoDB fails, return the record without storing
                import logging
                logging.warning(f"Failed to store prediction in MongoDB: {str(mongo_error)}")
                return jsonify({"record": {"prediction": record["prediction"], "images": record["images"]}}), 201
        else:
            # MongoDB not available, return record without storing
            return jsonify({"record": {"prediction": record["prediction"], "images": record["images"]}}), 201
    except Exception as error:
        error_msg = str(error)
        logger.error(f"Prediction failed: {error_msg}", exc_info=True)
        return jsonify({
            "message": f"Prediction failed: {error_msg}",
            "error": error_msg
        }), 500


def legacy_predict():
    logger.info("Legacy predict endpoint called")
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
