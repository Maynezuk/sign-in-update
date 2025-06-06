from fastapi import FastAPI, HTTPException, Depends, Header
from typing import Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
from models import Base, User
from database import engine, session_local
from schemas import UserCreate, User as DbUser
from jose import jwt
from datetime import datetime, timedelta, timezone


app = FastAPI()

# JWT конфигурация (пока бездарный секретный ключ побудет здесь)
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1 # Таймер существоания токена (для проверки ставлю на 1 минуту)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_credentials=True,
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

async def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization[7:]  # Убираем 'Bearer '

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/api/users/", response_model=DbUser)
async def create_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    try:
        db_user = User(
            name=user.name, surname=user.surname, patronymic=user.patronymic, login=user.login, password=user.password
        )
        db_user.password = pwd_context.hash(user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        raise HTTPException(status_code=404, detail='Login already used')



# sqlalchemy.exc.IntegrityError:

@app.post("/api/users/login")
async def login_user(user_data: dict, db: Session = Depends(get_db)):
    login = user_data.get('login')
    password = user_data.get('password')

    db_user = db.query(User).filter(User.login == login).first()
    if db_user is None or not pwd_context.verify(password, db_user.password):
        raise HTTPException(status_code=404, detail='User not found or incorrect password')

    access_token = create_access_token(
        data={
            "sub": db_user.login,
            "name": db_user.name,
            "surname": db_user.surname,
            "id": db_user.id,
            "timer_sec": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        },
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.get("/api/users/data")
async def read_current_user(current_user: dict = Depends(get_current_user)):
    # Проверка, что токен еще действителен
    if datetime.utcnow() > datetime.fromtimestamp(current_user["exp"]):
        raise HTTPException(status_code=401, detail="Token expired")
    return current_user
