from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.config.env_config import settings

# sqlite_file_name = "platepal.db"
# sqlite_url = f"sqlite:///{sqlite_file_name}"
# engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})
engine = create_async_engine(url=settings.DATABASE_URL, echo=True)


async def create_db_and_tables():
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


sessionDep = Depends(get_session)
