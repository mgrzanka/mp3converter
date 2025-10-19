from flask import Flask, request, abort
import json
from src.controllers.auth_controller import AuthController
from src.services.upload_download_service import UploadDownloadService


class UploadDownloadController(AuthController):
    def __init__(self, app: Flask) -> None:
        super().__init__(app)
        self.upload_download_service = UploadDownloadService(app)

    def create_api(self, parent_blueprint=None):
        blueprint = parent_blueprint or self.app
        super().create_api(blueprint)

        @blueprint.route("/upload", methods=["POST"])
        def upload():
            if not request.files or len(request.files.keys()) != 1:
                abort(400, 'Provide exactly one file to upload')
            auth = request.authorization
            if not auth or not auth.type.lower() == 'bearer':
                abort(401, 'Missing credentails')

            token = self.auth_service.validate(auth.token)
            email = json.loads(token).get('email')
            if not email:
                abort(401, 'Wrong JWT data')

            return self.upload_download_service.upload(request, email)

        @blueprint.route("/download", methods=["GET"])
        def dowload():
            auth = request.authorization
            if not auth or not auth.type.lower() == 'bearer':
                abort(401, 'Missing credentails')

            token = self.auth_service.validate(auth.token)
            mp3_fid = request.args.get('mp3_fid')

            if not mp3_fid:
                abort(401, 'No mp3_fid param')

            return self.upload_download_service.download(mp3_fid)
