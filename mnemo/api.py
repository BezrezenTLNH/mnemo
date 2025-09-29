from typing import Generator

from fastapi import Depends, FastAPI, HTTPException
from passlib.hash import bcrypt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from . import models
from .database import SessionLocal

app = FastAPI()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserCreate(BaseModel):
    email: str
    password: str


class CardCreate(BaseModel):
    question: str
    answer: str


@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = bcrypt.hash(user.password)
    new_user = models.User(email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "email": new_user.email}


@app.post("/cards")
def create_card(card: CardCreate, db: Session = Depends(get_db)):
    db_card = models.Card(question=card.question, answer=card.answer)
    if db_card:
        raise HTTPException(status_code=400, detail="Card already exists")
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return {"id": db_card.id, "question": db_card.question, "answer": db_card.answer}


@app.delete("/cards/{card_id}")
def delete_card(card_id: int, db: Session = Depends(get_db)):
    card = db.query(models.Card).get(card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    db.delete(card)
    db.commit()
    return {"ok": True}


@app.put("/cards/{card_id}")
def update_card(card_id: int, card: CardCreate, db: Session = Depends(get_db)):
    db_card = db.query(models.Card).get(card_id)
    if not db_card:
        raise HTTPException(status_code=404, detail="Card not found")
    db_card.front_text = card.front_text
    db_card.back_text = card.back_text
    db.commit()
    db.refresh(db_card)
    return db_card
