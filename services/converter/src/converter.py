import tempfile
from moviepy.editor import VideoFileClip
from src.mongo import Mongo

class Converter():
    def __init__(self, mongo: Mongo) -> None:
        self.mongo = mongo

    def convert(self, message):
        video = self.mongo.get_video(message["video_fid"])

        # read video
        video_temp_file = tempfile.NamedTemporaryFile()
        video_temp_file.write(video.read())
        audio = VideoFileClip(video_temp_file.name).audio
        video_temp_file.close()

        # write audio
        audio_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"
        if audio is not None:
            audio.write_audiofile(audio_path)
            with open(audio_path, "rb") as audio_file:
                return audio_file.read()
        else:
            raise ValueError("No audio track found in the video file.")
