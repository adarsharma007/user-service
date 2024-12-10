import logging
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from config.db import mongo

auth_blueprint = Blueprint("auth", __name__)

@auth_blueprint.route("/signup", methods=["POST"])
def signup():
    try:
        logging.info(f"Signup endpoint called with data: {request.json}")
        data = request.json
        if not data or not data.get("email") or not data.get("password"):
            logging.warning("Signup failed: Missing email or password.")
            return jsonify({"error": "Email and password are required"}), 400

        user = mongo.db.users.find_one({"email": data["email"]})
        if user:
            logging.warning(f"Signup failed: User {data['email']} already exists.")
            return jsonify({"error": "User already exists"}), 409

        hashed_password = generate_password_hash(data["password"])
        mongo.db.users.insert_one({"email": data["email"], "password": hashed_password})

        logging.info(f"User {data['email']} signed up successfully.")
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        logging.error(f"Error during signup: {str(e)}", exc_info=True)
        return jsonify({"error": "An unexpected error occurred"}), 500


@auth_blueprint.route("/login", methods=["POST"])
def login():
    try:
        logging.info(f"Login endpoint called with data: {request.json}")
        data = request.json
        if not data or not data.get("email") or not data.get("password"):
            logging.warning("Login failed: Missing email or password.")
            return jsonify({"error": "Email and password are required"}), 400

        user = mongo.db.users.find_one({"email": data["email"]})
        if not user or not check_password_hash(user["password"], data["password"]):
            logging.warning(f"Login failed: Invalid credentials for {data['email']}.")
            return jsonify({"error": "Invalid email or password"}), 401

        access_token = create_access_token(identity=data["email"])
        logging.info(f"User {data['email']} logged in successfully.")
        return jsonify({"access_token": access_token}), 200
    except Exception as e:
        logging.error(f"Error during login: {str(e)}", exc_info=True)
        return jsonify({"error": "An unexpected error occurred"}), 500


@auth_blueprint.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    try:
        current_user = get_jwt_identity()
        logging.info(f"Protected endpoint accessed by {current_user}.")
        return jsonify({"message": "Access granted", "user": current_user}), 200
    except Exception as e:
        logging.error(f"Error in protected endpoint: {str(e)}", exc_info=True)
        return jsonify({"error": "An unexpected error occurred"}), 500
