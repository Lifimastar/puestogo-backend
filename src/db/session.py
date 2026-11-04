from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.core.config import settings

engine = create_async_engine(settings.database_url, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Corregimos el tipo de retorno usando AsyncGenerator
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session