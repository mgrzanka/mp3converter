from gridfs import GridFS
from flask_pymongo import PyMongo
from flask import Flask
from bson import ObjectId
from src.config import Config


class Mongo:
    def __init__(self, app: Flask) -> None:
        mongo_video = PyMongo(app, uri=Config.MONGO_VIDEO_URI)
        mongo_mp3 = PyMongo(app, uri=Config.MONGO_MP3_URI)
        if mongo_video.db is None or mongo_mp3.db is None:
            raise RuntimeError("No database in mongoDB")

        self.grid_fs_video = GridFS(mongo_video.db)
        self.grid_fs_mp3 = GridFS(mongo_mp3.db)

    def put_video(self, data):
        fid = self.grid_fs_video.put(data)
        return str(fid)

    def delete_video(self, file_id: str):
        self.grid_fs_video.delete(ObjectId(file_id))

    def get_mp3(self, mp3_fid: str):
        return self.grid_fs_mp3.get(ObjectId(mp3_fid))

    def delete_mp3(self, mp3_fid: str):
        self.grid_fs_mp3.delete(ObjectId(mp3_fid))
