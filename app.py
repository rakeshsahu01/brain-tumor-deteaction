import os
import sys
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.info("Starting Brain Tumor Detection application...")

try:
    logger.info("Importing backend...")
    from backend import create_app
    logger.info("Backend imported successfully")
    
    logger.info("Creating Flask app...")
    app = create_app()
    logger.info("Flask app created successfully")
    
    # Add a simple home route
    @app.route('/')
    def home():
        return "App is running", 200
    
    # Add a simple health check endpoint
    @app.route('/health')
    def health():
        return {"status": "healthy"}, 200
    
except Exception as e:
    logger.error(f"Failed to initialize app: {str(e)}", exc_info=True)
    sys.exit(1)


if __name__ == "__main__":
    try:
        port = int(os.getenv("PORT", 5000))
        debug = os.getenv("FLASK_ENV") != "production"
        logger.info(f"Starting Flask app on port {port}, debug={debug}")
        app.run(host="0.0.0.0", port=port, debug=debug)
    except Exception as e:
        logger.error(f"Failed to start Flask app: {str(e)}", exc_info=True)
        sys.exit(1)
