# db.py

from functools import cache
from typing import AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine  # type: ignore
from sqlmodel.ext.asyncio.session import AsyncSession

from .config import get_settings


@cache
def get_engine() -> AsyncEngine:
    settings = get_settings()
    return create_async_engine(settings.db_url, echo=settings.echo)


@cache
def get_session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def get_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    async_session_maker = request.app.state.async_session_maker
    async with async_session_maker() as session:
        yield session
