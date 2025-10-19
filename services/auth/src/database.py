from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.sql import func
from datetime import datetime
import uuid


class Database:
    class Base(DeclarativeBase):
        pass

    def __init__(self, app: Flask):
        self.db = SQLAlchemy(app, model_class=self.Base)
        self.migrate = Migrate(app, self.db, directory='../migrations')

    class User(Base):
        __tablename__ = 'users'

        uuid: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
        email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
        password: Mapped[str] = mapped_column(String(200), nullable=False)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
