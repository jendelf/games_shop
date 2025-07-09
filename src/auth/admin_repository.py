from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import User
from src.role import Role

async def get_all_users(session: AsyncSession):
    result = await session.execute(select(User))
    return result.scalars().all()

async def ban_user(user_id: int, session: AsyncSession):
    user = await session.get(User, user_id)
    if not user:
        return f"User with ID {user_id} not found"
    user.disabled = True
    await session.commit()
    return f"User {user.username} has been banned"

async def update_user_role(user_id: int, new_role: Role, session: AsyncSession):
    user = await session.get(User, user_id)
    if not user:
        return f"User with ID {user_id} not found"
    user.role = new_role
    await session.commit()
    return f"User {user.username} role updated to {new_role.value}"