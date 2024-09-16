from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import TIMESTAMP
from sqlalchemy import func
from sqlalchemy.orm import relationship

from .base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    links = relationship('UserLinks', back_populates='user')


class UserLinks(BaseModel):
    __tablename__ = 'user_links'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    link_id = Column(String(255), nullable=False)
    institution = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    user = relationship('User', back_populates='links')
