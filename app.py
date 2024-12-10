import logging
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager  # Import JWTManager
from config.db import initialize_db
from services.auth import auth_blueprint
from dotenv import load_dotenv
import os
logging.info(f"Current working directory: {os.getcwd()}")
app = Flask(__name__)
load_dotenv()
# Load configurations
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

# Initialize JWT Manager
jwt = JWTManager(app)  # Add this line

log_file_path = os.path.join(os.path.dirname(__file__), "user-service.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file_path),  # Use absolute path for logging
        logging.StreamHandler()
    ]
)

logging.info("Logging setup complete. Test log entry.")


# Initialize database
initialize_db(app)

# Register blueprints
app.register_blueprint(auth_blueprint, url_prefix="/auth")

@app.route("/")
def health_check():
    return jsonify({"status": "User-service is running"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
