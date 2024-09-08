from flask import g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config


engine = create_engine(Config.DATABASE_URI)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

def init_db():
    def get_db():
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = SessionLocal()
        return db
    
    return engine, get_db