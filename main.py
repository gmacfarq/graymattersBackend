from fastapi import FastAPI, Depends, Request, HTTPException
from starlette.status import HTTP_403_FORBIDDEN

import models
from models import User, Book
from database import SessionLocal, engine
from schemas import LoginInfo

from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)


app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # The origin of your React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key="!secret")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def admin_required(request: Request):
    username = request.session.get("username")
    is_admin = request.session.get("is_admin", False)

    if not username or not is_admin:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )

@app.get("/")
def home():
    return {"message": "Home"}

@app.post("/register")
def register(request: Request, user_data: LoginInfo, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()
    if user is not None:
        raise HTTPException(status_code=404, detail="User alrady exists")
    new_user = User(username=user_data.username)
    new_user.set_password(user_data.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    request.session['username'] = new_user.username
    request.session['is_admin'] = new_user.is_admin

    return {"message": "User created"}

@app.post("/login")
def login(request: Request, user_data: LoginInfo, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.check_password(user_data.password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    request.session['username'] = user.username
    request.session['is_admin'] = user.is_admin

    return {"message": "Logged in"}

@app.get("/logout")
def logout(request: Request):
    request.session.pop('username', None)
    return {"message": "Logged out"}

@app.get("/library")
def library(request: Request, db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return {"books": books}

@app.post("/library")
async def add_book(request: Request, db: Session = Depends(get_db), user: str = Depends(admin_required)):
    book_data = await request.json()
    new_book = Book(**book_data)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return {"message": "Book added"}

@app.get("/library/{book_id}")
def book():
    return {"message": "Book {book_id}"}
