from flask import jsonify
from werkzeug.exceptions import HTTPException


def register_error_handler(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return jsonify({
                "error": e.name,
                "message": e.description,
                "code": e.code
            }), e.code

        return jsonify({
            "error": "Internal Server Error",
            "message": str(e) if str(e) else "Unknown error",
            "code": 500
        }), 500
