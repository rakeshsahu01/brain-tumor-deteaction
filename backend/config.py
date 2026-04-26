import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "brain-tumor-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "brain-tumor-jwt-secret")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017")
    DB_NAME = os.getenv("DB_NAME", "brain_tumor_ai")
    MODEL_PATH = os.getenv("MODEL_PATH", "model.h5")
    MODEL_JSON_PATH = os.getenv("MODEL_JSON_PATH", "model.json")
    MODEL_WEIGHTS_PATH = os.getenv("MODEL_WEIGHTS_PATH", "model.h5")
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
