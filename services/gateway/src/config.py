import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

class Config:
    AUTH_SERVICE_HOST = os.getenv('AUTH_SERVICE_HOST')
    RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', '')
    RABBITMQ_PORT = os.getenv('RABBITMQ_PORT', int(5672))
    RABBITMQ_USER = os.getenv('RABBITMQ_USER', '')
    RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', '')

    MONGO_USER=os.getenv('MONGO_USER')
    MONGO_PASSWORD=os.getenv('MONGO_PASSWORD')
    MONGO_HOST = os.getenv('MONGO_HOST')
    MONGO_PORT = os.getenv('MONGO_PORT', int(27017))

    if not AUTH_SERVICE_HOST:
        raise RuntimeError('AUTH_SERVICE_HOST not provided')
    if not MONGO_USER or not MONGO_PASSWORD or not MONGO_HOST:
        raise RuntimeError('Mongo data not provided')
    if not RABBITMQ_HOST or not RABBITMQ_USER or not RABBITMQ_PASSWORD:
        raise RuntimeError('Rabbit data not provided')

    PORT = int(os.getenv('PORT', 8080))
    MONGO_VIDEO_URI = f'mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/videos?authSource=admin'
    MONGO_MP3_URI = f'mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/mp3s?authSource=admin'
