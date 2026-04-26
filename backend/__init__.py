from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from backend.config import Config
from backend.routes.auth_routes import auth_bp
from backend.routes.history_routes import history_bp
from backend.routes.patient_routes import patient_bp
from backend.routes.prediction_routes import prediction_bp
from backend.routes.report_routes import report_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    JWTManager(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(report_bp)

    @app.get("/home")
    def home():
        return jsonify({"message": "Brain Tumor AI backend is running"})

    return app
