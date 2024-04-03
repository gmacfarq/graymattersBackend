from pydantic import BaseModel

class Book(BaseModel):
    id: int
    title: str
    rating: int
    review: str
    author: str
    start_date: str
    finish_date: str
    genre: str
    photo_uri: str

class LoginInfo(BaseModel):
    username: str
    password: str

