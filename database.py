from sqlalchemy import create_engine
from  sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///clinic.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},   # SQLite 专用
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)