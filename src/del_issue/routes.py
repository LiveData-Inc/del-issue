# routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .db import get_session
from .models import User

router = APIRouter()


@router.get("/users/{user_id}", response_model=User)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_session)
) -> User:
    result = await session.exec(select(User).where(User.id == user_id))
    user: User | None = result.first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/users/", response_model=User)
async def create_user(
    new_user: User,
    session: AsyncSession = Depends(get_session)
) -> User | None:
    try:
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
    except Exception as e:
        print(f"Error creating user: {e}")
