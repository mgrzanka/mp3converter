from flask import abort, Flask, send_file, after_this_request
from flask.wrappers import Request
from src.mongo import Mongo
from src.rabbitmq import RabbitMq


class UploadDownloadService:
    def __init__(self, app: Flask) -> None:
        self.mongo_service = Mongo(app)
        self.rabbitmq = RabbitMq()

    def upload(self, request: Request, email: str):
        message: dict[str, str | None] = {
            "video_fid": None,
            "mp3_fid": None,
            "email": None
        }

        for _, file in request.files.items():
            try:
                fid = self.mongo_service.put_video(file)
            except Exception as e:
                abort(500, f'Error while putting file in mongoDB: {e}')

            message = {
                "video_fid": fid,
                "mp3_fid": '',
                "email": email
            }
            try:
                self.rabbitmq.publish_message(message, 'video')
            except Exception as e:
                self.mongo_service.delete_video(str(fid))
                abort(500, f'Error putting message in rabbitmq: {e}')

        return {"message": message}

    def download(self, mp3_fid: str):
        try:
            mp3_file = self.mongo_service.get_mp3(mp3_fid)
            return send_file(mp3_file, download_name=f"{mp3_fid}.mp3")
        except Exception as e:
            print(f"Error while sending file from mongodb: {e}")
            abort(500, "Error while sending file from mongodb")
