from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))


class Config:
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", '')
    RABBITMQ_USER = os.getenv("RABBITMQ_USER", '')
    RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", '')
    MP3_QUEUE_NAME = os.getenv("MP3_QUEUE_NAME", "mp3")

    SENDER_EMAIL = os.getenv("SENDER_EMAIL", '')
    SENDER_EMAIL_PASSWORD = os.getenv("SENDER_EMAIL_PASSWORD", '')

    MP3_DOWLOAD_ENDPOINT = os.getenv("MP3_DOWLOAD_ENDPOINT")

    if not RABBITMQ_HOST or not RABBITMQ_USER or not RABBITMQ_PASSWORD:
        raise RuntimeError("No rabbitmq params in .env file")
    if not SENDER_EMAIL or not SENDER_EMAIL_PASSWORD:
        raise RuntimeError("No sender email or sender email password in .env file")
