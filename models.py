from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from database import Base
import bcrypt

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    is_admin = Column(Boolean, default=False)

    def set_password(self, password):
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        self.password_hash = hashed_password.decode('utf-8')

    def check_password(self, password):
        password_bytes = password.encode('utf-8')
        hashed_password_bytes = self.password_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_password_bytes)



class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    rating = Column(Integer)
    review = Column(String)
    author = Column(String)
    start_date = Column(DateTime)
    finish_date = Column(DateTime, default = None)
    genre = Column(String)
    photo_uri = Column(String)