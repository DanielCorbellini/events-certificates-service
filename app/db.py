import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

DB_HOST = os.getenv("DATASOURCE_HOST")
DB_PORT = os.getenv("DATASOURCE_PORT")
DB_NAME = os.getenv("DATASOURCE_DB")
DB_USER = os.getenv("DATASOURCE_USERNAME")
DB_PASS = os.getenv("DATASOURCE_PASSWORD")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
