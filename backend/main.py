from fastapi import FastAPI, HTTPException, Depends, Response, Request
from typing import Optional
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
from models import Base, User
from database import engine, session_local
from schemas import UserCreate, User as DbUser
from jose import jwt
from datetime import datetime, timedelta


app = FastAPI()

# JWT конфигурация (пока бездарный сикретный ключ побудет здесь)
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if token is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

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

    access_token = create_access_token(
        data={
            "sub": db_user.login,
            "name": db_user.name,
            "surname": db_user.surname,
            "id": db_user.id
        },
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=False  # Для разработки! Если нужно, могу вернуть обратно в True
    )

    return {"message": "Login successful",}

@app.get("/api/users/me")
async def read_current_user(current_user: dict = Depends(get_current_user)):
    return current_user

@app.post("/api/users/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logout successful"}

@app.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello {current_user['name']}", "user": current_user}