from fastapi import FastAPI, HTTPException, Depends, Header, status
from typing import Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
from models import Base, User, RefreshToken
from database import engine, session_local
from schemas import UserCreate, DbUser, RefreshTokenBase
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone


app = FastAPI()

# JWT конфигурация (пока бездарный секретный ключ побудет здесь)
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1 # Таймер существоания токена (для проверки ставлю на 1 минуту)
REFRESH_TOKEN_EXPIRE_DAYS = 30

TOKEN_TYPE_ACCESS = "access"
TOKEN_TYPE_REFRESH = "refresh"

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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


def create_token(data: dict, expires_delta: Optional[timedelta] = None, token_type: str = TOKEN_TYPE_ACCESS):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({
        "exp": expire,
        "type": token_type
    })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(authorization: str = Header(...), db: Session = Depends(get_db)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization[7:]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != TOKEN_TYPE_ACCESS:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
                headers={"WWW-Authenticate": "Bearer"},
            )

        login: str = payload.get("sub")
        if login is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = db.query(User).filter(User.login == login).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def create_refresh_token_record(db: Session, user: User, token: str, expires_delta: timedelta):
    expires_at = datetime.now(timezone.utc) + expires_delta
    db_token = RefreshToken(
        token=token,
        user_id=user.id,
        expires_at=expires_at
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


async def validate_refresh_token(refresh_token: str, db: Session):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != TOKEN_TYPE_REFRESH:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )

        login: str = payload.get("sub")
        if login is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        user = db.query(User).filter(User.login == login).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        token_record = db.query(RefreshToken).filter(
            RefreshToken.token == refresh_token,
            RefreshToken.user_id == user.id,
            RefreshToken.expires_at > datetime.now(timezone.utc)
        ).first()

        if not token_record:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token not found or expired",
            )

        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired",
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )


@app.post("/api/refresh")
async def refresh_token(request: RefreshTokenBase, db: Session = Depends(get_db)):
    user = await validate_refresh_token(request.refresh_token, db)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(
        data={
            "sub": user.login,
            "name": user.name,
            "surname": user.surname,
            "id": user.id,
            "timer_sec": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        },
        expires_delta=access_token_expires,
        token_type=TOKEN_TYPE_ACCESS
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.post("/api/registration", response_model=DbUser)
async def create_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    try:
        db_user = User(
            name=user.name, surname=user.surname, patronymic=user.patronymic,
            login=user.login, password=user.password
        )
        db_user.password = pwd_context.hash(user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        raise HTTPException(status_code=400, detail='Login already used')


def cleanup_expired_tokens(db: Session):
    db.query(RefreshToken).filter(
        RefreshToken.expires_at < datetime.now(timezone.utc)
    ).delete()
    db.commit()


@app.post("/api/login")
async def login_user(user_data: dict, db: Session = Depends(get_db)):
    try:
        login = user_data.get('login')
        password = user_data.get('password')

        db_user = db.query(User).filter(User.login == login).first()
        if db_user is None or not pwd_context.verify(password, db_user.password):
            raise HTTPException(status_code=401, detail='User not found or incorrect password')

        try:
            db.query(RefreshToken).filter(RefreshToken.user_id == db_user.id).delete()
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail='Failed to clean old tokens')

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_token(
            data={
                "sub": db_user.login,
                "name": db_user.name,
                "surname": db_user.surname,
                "id": db_user.id,
                "timer_sec": ACCESS_TOKEN_EXPIRE_MINUTES * 60
            },
            expires_delta=access_token_expires,
            token_type=TOKEN_TYPE_ACCESS
        )

        refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        refresh_token = create_token(
            data={"sub": db_user.login},
            expires_delta=refresh_token_expires,
            token_type=TOKEN_TYPE_REFRESH
        )

        create_refresh_token_record(db, db_user, refresh_token, refresh_token_expires)

        return {
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/data")
async def read_current_user(current_user: dict = Depends(get_current_user)):
    return current_user


@app.post("/api/logout")
async def logout(request: RefreshTokenBase, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(request.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        login = payload.get("sub")

        if not login:
            raise HTTPException(status_code=400, detail="Invalid token")

        result = db.query(RefreshToken).filter(
            RefreshToken.token == request.refresh_token
        ).delete()

        if not result:
            raise HTTPException(status_code=404, detail="Token not found")

        db.commit()
        return {"message": "Logged out successfully"}
    except jwt.ExpiredSignatureError:
        db.query(RefreshToken).filter(
            RefreshToken.token == request.refresh_token
        ).delete()
        db.commit()
        return {"message": "Logged out successfully (token was expired)"}
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
