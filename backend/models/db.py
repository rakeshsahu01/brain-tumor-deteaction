from pymongo import MongoClient
from backend.config import Config


client = MongoClient(Config.MONGO_URI)
db = client[Config.DB_NAME]

users_collection = db["users"]
history_collection = db["prediction_history"]
patients_collection = db["patients"]
