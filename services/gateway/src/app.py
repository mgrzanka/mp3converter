from flask import Flask
from src.config import Config
from src.controllers.gateway_controller import GatewayController
from src.exceptions.exception_handler import register_error_handler


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_error_handler(app)
    controller = GatewayController(app)
    controller.create_gateway_api()

    return app


app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.PORT)
