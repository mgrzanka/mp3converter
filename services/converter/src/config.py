import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

class Config:
    MONGO_HOST = os.getenv("MONGO_HOST")
    MONGO_USER = os.getenv("MONGO_USER")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", '')
    RABBITMQ_USER = os.getenv("RABBITMQ_USER", 'guest')
    RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", 'guest')

    VIDEOS_QUEUE_NAME = os.getenv("VIDEOS_QUEUE_NAME", "video")

    if not MONGO_HOST:
        raise RuntimeError("No MONGO_HOST in .env file")
    if not RABBITMQ_PASSWORD:
        raise RuntimeError("No RABBIMQ_PASSWORD in .env file")

    MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:27017?authSource=admin"
