from fastapi import FastAPI,HTTPException, Depends, Response
from typing import Optional
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
from models import Base, User
from database import engine, session_local
from schemas import UserCreate, User as DbUser
from authx import AuthX, AuthXConfig


app = FastAPI()


config = AuthXConfig()
config.JWT_SECRET_KEY = "secret_key"
config.JWT_ALGORITHM = "HS256"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)


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
async def login_user(user_data: dict, db: Session = Depends(get_db), response: Response = None):
    login = user_data.get('login')
    password = user_data.get('password')

    db_user = db.query(User).filter(User.login == login).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')

    if not pwd_context.verify(password, db_user.password):
        raise HTTPException(status_code=401, detail='Incorrect password')

    token = security.create_access_token(uid=str(db_user.id))

    security.set_access_cookies(token, response)

    return {
        "message": "Login successful",
        "user_id": db_user.id,
        "user_name": db_user.name,
        "user_surname": db_user.surname,
        "access_token": token,
        "token_type": "bearer"
    }



@app.get("/protected", dependencies=[Depends(security.access_token_required)])
def get_protected():
    return {"message": "Hello World"}