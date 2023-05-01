from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import declarative_base, relationship

from src.database.db import engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(15), nullable=False)
    avatar = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())
    refresh_token = Column(String(255), nullable=True)


class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, nullable=False)
    lastname = Column(String, index=True, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)
    birthday = Column(DateTime, index=True, nullable=True)
    additional_info = Column(String, index=True)
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now())
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="contacts")


Base.metadata.create_all(bind=engine)


