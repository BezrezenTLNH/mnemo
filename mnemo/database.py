import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
db = os.getenv("POSTGRES_DB")
host = os.getenv("POSTGRES_HOST", "localhost")
port = os.getenv("POSTGRES_PORT", "5432")

engine = create_engine(
    f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}", echo=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
