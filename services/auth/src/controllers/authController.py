from flask import Blueprint, Flask, request, abort

from src.database import Database
from src.services.authService import AuthService


class AuthController:
    def __init__(self, database: Database):
        self.auth_service = AuthService(database)

    def create_auth_api(self, app: Flask):
        auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")

        @auth_blueprint.route("/login", methods=["POST"])
        def login():
            auth = request.authorization
            if not auth or auth.type.lower() != "basic" or not auth.username or not auth.password:
                abort(401, "Missing credentials")

            return self.auth_service.login(auth.username, auth.password)

        @auth_blueprint.route("/register", methods=["POST"])
        def register():
            request_body = request.get_json()
            email = request_body.get("email")
            password = request_body.get("password")
            if not email or not password:
                abort(400, "Missing data")

            return self.auth_service.register(email, password)

        @auth_blueprint.route("/validate", methods=["POST"])
        def validate_jwt_token():
            auth = request.authorization
            if not auth or auth.type.lower() != "bearer":
                abort(400, "No JWT token to validate")

            return self.auth_service.verify_jwt(auth.token)


        app.register_blueprint(auth_blueprint)
