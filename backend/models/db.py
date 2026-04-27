from pymongo import MongoClient
from backend.config import Config
import logging
import ssl

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
        logger.info(f"Connecting to MongoDB: {Config.MONGO_URI}")
        
        # Create SSL context to handle TLS issues in containerized environments
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = True
        ssl_context.verify_mode = ssl.CERT_REQUIRED
        
        _client = MongoClient(
            Config.MONGO_URI,
            serverSelectionTimeoutMS=5000,
            tlsCAFile=None,
            ssl_context=ssl_context
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
