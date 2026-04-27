import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from backend.config import Config
from backend.routes.auth_routes import auth_bp
from backend.routes.history_routes import history_bp
from backend.routes.patient_routes import patient_bp
from backend.routes.prediction_routes import prediction_bp
from backend.routes.report_routes import report_bp


def create_app():
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), '..', 'client', 'build', 'static'), static_url_path='/static')
    app.config.from_object(Config)

    CORS(app)
    JWTManager(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(report_bp)

    # Serve React frontend
    @app.route('/')
    def serve_index():
        build_dir = os.path.join(os.path.dirname(__file__), '..', 'client', 'build')
        if os.path.exists(build_dir):
            return send_from_directory(build_dir, 'index.html')
        return jsonify({"message": "Brain Tumor AI backend is running"}), 200

    @app.route('/<path:path>')
    def serve_static_or_react(path):
        build_dir = os.path.join(os.path.dirname(__file__), '..', 'client', 'build')
        if os.path.exists(os.path.join(build_dir, path)):
            return send_from_directory(build_dir, path)
        # Serve index.html for React Router SPA
        if os.path.exists(os.path.join(build_dir, 'index.html')):
            return send_from_directory(build_dir, 'index.html')
        return jsonify({"error": "Not found"}), 404

    return app
