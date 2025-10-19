import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))


class Config:
    JWT_SIGNING_KEY = os.getenv("JWT_SIGNING_KEY", "")
    DB_HOST=os.getenv('DB_HOST')
    DB_PORT=os.getenv('DB_PORT')
    DB_NAME=os.getenv('DB_NAME')
    DB_USER=os.getenv('DB_USER')
    DB_PASSWORD=os.getenv('DB_PASSWORD')

    if not DB_HOST or not DB_PORT or not DB_NAME or not DB_USER or not DB_PASSWORD:
        raise RuntimeError("Database connection environment variable(s) are not set")
    if not JWT_SIGNING_KEY:
        raise RuntimeError("JWT_SIGNING_KEY variable is not set")

    PORT = int(os.getenv("FLASK_RUN_PORT", 8080))
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
