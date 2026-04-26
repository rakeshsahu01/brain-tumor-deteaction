from flask import Blueprint

from backend.controllers.auth_controller import login, signup


auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")
auth_bp.post("/signup")(signup)
auth_bp.post("/login")(login)
