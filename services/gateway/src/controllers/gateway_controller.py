from flask import Flask, Blueprint
from src.controllers.upload_download_controller import UploadDownloadController


class GatewayController(UploadDownloadController):
    def __init__(self, app: Flask) -> None:
        super().__init__(app)

    def create_gateway_api(self):
        blueprint = Blueprint('gateway', __name__, url_prefix='/gateway')
        super().create_api(blueprint)
        self.app.register_blueprint(blueprint)
