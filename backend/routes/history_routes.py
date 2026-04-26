from flask import Blueprint
from flask_jwt_extended import jwt_required

from backend.controllers.history_controller import get_history


history_bp = Blueprint("history", __name__, url_prefix="/api/history")
history_bp.get("/")(jwt_required()(get_history))
