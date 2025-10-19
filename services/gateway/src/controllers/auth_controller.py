from flask import Flask, Blueprint, request, abort
from src.services.auth_service import AuthService

class AuthController:
    def __init__(self, app: Flask) -> None:
        self.app = app
        self.auth_service = AuthService()

    def create_api(self, parent_blueprint=None):
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
            return self.auth_service.register(request_body)

        if parent_blueprint:
            parent_blueprint.register_blueprint(auth_blueprint)
        else:
            self.app.register_blueprint(auth_blueprint)
