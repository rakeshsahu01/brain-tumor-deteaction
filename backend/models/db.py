from pymongo import MongoClient
from backend.config import Config
import logging

logger = logging.getLogger(__name__)

# Lazy MongoDB connection
_mongo_initialized = False
_client = None
_db = None
_users_collection = None
_history_collection = None
_patients_collection = None


def _initialize_mongo():
    global _mongo_initialized, _client, _db, _users_collection, _history_collection, _patients_collection
    
    if _mongo_initialized:
        return
    
    try:
        logger.info("Connecting to MongoDB...")
        
        # Standard connection with timeout settings and SSL support
        _client = MongoClient(
            Config.MONGO_URI,
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=15000,
            retryWrites=True,
            ssl=True,
            tlsInsecure=False,
            tlsCAFile=None,  # Use system default certificates
        )
        # Verify connection
        _client.admin.command('ping')
        logger.info("MongoDB connected successfully")
        _db = _client[Config.DB_NAME]
        _users_collection = _db["users"]
        _history_collection = _db["prediction_history"]
        _patients_collection = _db["patients"]
        _mongo_initialized = True
    except Exception as e:
        logger.warning(f"MongoDB connection failed (will retry on use): {str(e)}")
        _mongo_initialized = False


def get_users_collection():
    if not _mongo_initialized:
        _initialize_mongo()
    return _users_collection


def get_history_collection():
    if not _mongo_initialized:
        _initialize_mongo()
    return _history_collection


def get_patients_collection():
    if not _mongo_initialized:
        _initialize_mongo()
    return _patients_collection


# For backward compatibility, try to initialize on import but don't fail
try:
    _initialize_mongo()
except Exception as e:
    logger.warning(f"MongoDB initialization deferred: {str(e)}")

# Fallback to None if not available - controllers will handle gracefully
users_collection = _users_collection
history_collection = _history_collection
patients_collection = _patients_collection
