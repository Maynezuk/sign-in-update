from fastapi import FastAPI,HTTPException, Depends
from typing import Optional
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
from models import Base, User
from database import engine, session_local
from schemas import UserCreate, User as DbUser


app = FastAPI()


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# При создании пользователя


# При проверке пароля


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/users/", response_model=DbUser)
async def create_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    db_user = User(
        name=user.name, surname=user.surname, middlename=user.middlename, login=user.login, password=user.password
    )
    db_user.password = pwd_context.hash(user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@app.post("/api/users/login")
async def login_user(user_data: dict, db: Session = Depends(get_db)):
    login = user_data.get('login')
    password = user_data.get('password')

    db_user = db.query(User).filter(User.login == login).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')

    if not pwd_context.verify(password, db_user.password):
        raise HTTPException(status_code=401, detail='Incorrect password')

    return {"message": "Login successful", "user_id": db_user.id}



# @app.get("/protected")
# def protected():
#     ...