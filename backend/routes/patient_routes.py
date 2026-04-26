from flask import Blueprint
from flask_jwt_extended import jwt_required

from backend.controllers.patient_controller import create_patient, get_patient


patient_bp = Blueprint("patient", __name__, url_prefix="/api/patients")
patient_bp.post("/")(jwt_required()(create_patient))
patient_bp.get("/<patient_id>")(jwt_required()(get_patient))
