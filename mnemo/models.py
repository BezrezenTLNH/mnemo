from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    cards = relationship("UserCard", back_populates="user")


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    answer = Column(String(1000), nullable=False)

    users = relationship("UserCard", back_populates="card")


class UserCard(Base):
    __tablename__ = "user_cards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    card_id = Column(Integer, ForeignKey("cards.id"))
    progress_level = Column(Integer, default=0)
    next_review_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="cards")
    card = relationship("Card", back_populates="users")
