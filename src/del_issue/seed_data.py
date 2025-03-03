# seed_data.py

from typing import cast

from sqlalchemy.orm import sessionmaker
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import User


async def seed_data(async_session_factory: sessionmaker) -> None:
    async with async_session_factory() as _session:
        session = cast(AsyncSession, _session)
        stmt = select(User).limit(1)
        result = await session.exec(stmt)
        existing = result.first()
        if existing:
            return  # already have a user

        # Insert a sample user
        usr = User(
            first_name="Alice",
            last_name="Test",
            sex="F"
        )
        session.add(usr)
        await session.commit()
