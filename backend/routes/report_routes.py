from flask import Blueprint
from flask_jwt_extended import jwt_required

from backend.controllers.report_controller import download_report


report_bp = Blueprint("report", __name__, url_prefix="/api/report")
report_bp.get("/<record_id>/download")(jwt_required()(download_report))
