import bcrypt, jwt, datetime
from flask import abort
import re

from src.config import Config
from src.database import Database
from src.repositories.authRepository import AuthRepository


class AuthService:
    def __init__(self, database: Database):
        self.auth_repository = AuthRepository(database)

    def login(self, email: str, password: str):
        user = self.auth_repository.get_user_by_email(email)
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            token = self._generate_jwt(user.email)
            return {"bearer": token}

        return abort(401, "Wrong email or password")


    def register(self, email: str, password: str):
        if not self._is_valid_email(email):
            abort(400, "Invalid email address")

        existing_user = self.auth_repository.get_user_by_email(email)
        if existing_user:
            abort(400, "Email already used")

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        created_user = self.auth_repository.create_user(email, hashed_password)
        token = self._generate_jwt(created_user.email)
        return {"bearer": token}

    def verify_jwt(self, jwt_data):
        try:
            return jwt.decode(jwt=jwt_data, key=Config.JWT_SIGNING_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            abort(401, "Token expired")
        except jwt.InvalidTokenError:
            abort(403, "Invalid token")

    def _generate_jwt(self, email: str):
        return jwt.encode(
            payload={
            "email": email,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1),
            "iat": datetime.datetime.now(datetime.timezone.utc)
            },
            key=Config.JWT_SIGNING_KEY,
            algorithm="HS256"
        )

    def _is_valid_email(self, email: str) -> bool:
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        return re.match(email_regex, email) is not None
