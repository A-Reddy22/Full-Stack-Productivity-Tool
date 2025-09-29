from sqlalchemy import select
from .db import SessionLocal
from .models import Priority

DEFAULT_PRIORITIES = [
    {"name": "High", "rank": 1},
    {"name": "Medium", "rank": 2},
    {"name": "Low", "rank": 3},
]

def seed_defaults() -> None:
    db = SessionLocal()
    try:
        existing = {p.name for p in db.execute(select(Priority)).scalars().all()}
        to_add = [Priority(**p) for p in DEFAULT_PRIORITIES if p["name"] not in existing]
        if to_add:
            db.add_all(to_add)
            db.commit()
    finally:
        db.close()
