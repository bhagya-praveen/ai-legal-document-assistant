from flask import Blueprint, request
from werkzeug.security import generate_password_hash

from database.db import db
from models.user import User

from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth"
)


@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    if not data:
        return {
            "message": "Request body is required"
        }, 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return {
            "message": "Username, email and password are required"
        }, 400

    existing_user = User.query.filter_by(
        email=email
    ).first()

    if existing_user:
        return {
            "message": "Email already registered"
        }, 409

    password_hash = generate_password_hash(password)

    user = User(
        username=username,
        email=email,
        password_hash=password_hash
    )

    db.session.add(user)
    db.session.commit()

    return {
        "message": "User registered successfully",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }, 201



@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return {
            "message": "Request body is required"
        }, 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {
            "message": "Email and password are required"
        }, 400

    user = User.query.filter_by(
        email=email
    ).first()

    if not user:
        return {
            "message": "Invalid email or password"
        }, 401

    if not check_password_hash(
        user.password_hash,
        password
    ):
        return {
            "message": "Invalid email or password"
        }, 401

    access_token = create_access_token(
        identity=str(user.id)
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }, 200


