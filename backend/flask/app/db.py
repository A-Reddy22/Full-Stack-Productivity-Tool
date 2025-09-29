import os
from typing import List
from flask import Flask
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")

engine = create_engine(
    DATABASE_URL,
    future=True,
    pool_pre_ping=True,
)

SessionLocal = scoped_session(
    sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
)

Base = declarative_base()

def init_cors(app: Flask) -> None:
    origins_env = os.getenv("CORS_ALLOW_ORIGINS", "*")
    origins: List[str] = [o.strip() for o in origins_env.split(",") if o.strip()]
    if not origins:
        origins = ["*"]
    CORS(app, resources={r"/api/*": {"origins": origins}}, supports_credentials=True)

def init_db() -> None:
    from .models import Priority, Task  # noqa: F401
    Base.metadata.create_all(bind=engine)
