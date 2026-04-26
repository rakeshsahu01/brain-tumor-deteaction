from flask import Blueprint
from flask_jwt_extended import jwt_required

from backend.controllers.prediction_controller import create_prediction, legacy_predict


prediction_bp = Blueprint("prediction", __name__)
prediction_bp.post("/api/predict")(jwt_required()(create_prediction))
prediction_bp.post("/")(legacy_predict)
