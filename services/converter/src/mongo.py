from pymongo import MongoClient
from gridfs import GridFS
from bson import ObjectId
from src.config import Config

class Mongo:
    def __init__(self) -> None:
        client = MongoClient(host=Config.MONGO_URI)
        videos_db = client.get_database("videos")
        mp3s_db = client.get_database("mp3s")
        self.videos_fs = GridFS(videos_db)
        self.mp3s_fs = GridFS(mp3s_db)

    def put_mp3(self, audioFile):
        return str(self.mp3s_fs.put(audioFile))

    def delete_mp3(self, mp3_fid):
        self.mp3s_fs.delete(ObjectId(mp3_fid))

    def get_video(self, fid: str):
        return self.videos_fs.get(ObjectId(fid))
