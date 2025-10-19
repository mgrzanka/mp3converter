from src.database import Database


class AuthRepository():
    def __init__(self, database: Database):
        self.database = database

    def get_user_by_email(self, email: str):
        return self.database.db.session.query(
                self.database.User
            ).filter_by(email=email).first()

    def create_user(self, email: str, hashed_password: bytes):
        user = Database.User(email=email, password=hashed_password.decode('utf-8'))
        self.database.db.session.add(user)
        self.database.db.session.commit()
        return user
