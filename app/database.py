from fastapi import Depends
from sqlmodel import create_engine, SQLModel, Session
from typing import Annotated

sqlite_file_name = "platepal.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)  # Create tables in the database

def get_session():
    with Session(engine) as session:
        yield session


sessionDep = Annotated[Session, Depends(get_session)]