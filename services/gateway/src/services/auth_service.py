import requests
import json
from flask import abort
from src.config import Config

class AuthService:
    def login(self, email: str, password: str):
        auth_service_response = requests.post(
            f'{Config.AUTH_SERVICE_HOST}/auth/login',
            auth=(email, password)
        )

        if auth_service_response.text and auth_service_response.status_code == 200:
            try:
                return json.loads(auth_service_response.text)
            except Exception as e:
                abort(500, f"Error while parsing auth service response: {e}")

        abort(auth_service_response.status_code, auth_service_response.text)

    def register(self, request_body):
        auth_service_response = requests.post(
            f'{Config.AUTH_SERVICE_HOST}/auth/register',
            headers={'Content-Type': 'application/json'},
            json=request_body
        )

        if auth_service_response.status_code == 200:
            try:
                return json.loads(auth_service_response.text)
            except Exception as e:
                abort(500, f"Error while parsing auth service response: {e}")

        abort(auth_service_response.status_code, auth_service_response.text)

    def validate(self, bearer):
        auth_service_response = requests.post(
            f'{Config.AUTH_SERVICE_HOST}/auth/validate',
            headers={"Authorization": f"Bearer {bearer}"}
        )

        if auth_service_response.status_code == 200:
            return auth_service_response.text

        abort(auth_service_response.status_code, auth_service_response.text)
