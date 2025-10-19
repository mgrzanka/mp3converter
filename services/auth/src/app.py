from flask import Flask
from src.exceptions.exeptionHandler import register_error_handler
from src.database import Database
from src.controllers.authController import AuthController
from src.config import Config


def createApp():
    app = Flask(__name__)
    app.config.from_object(Config)
    database = Database(app)
    authController = AuthController(database)
    authController.create_auth_api(app)
    register_error_handler(app)

    return app


app = createApp()
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=Config.PORT)
