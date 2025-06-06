from sqlalchemy import Column, Integer, String, ForeignKey, Nullable
from sqlalchemy.sql.operators import truediv

# from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    patronymic = Column(String)
    login = Column(String, index=True, unique=True)
    password = Column(String)


