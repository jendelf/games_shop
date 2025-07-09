from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user(session: AsyncSession, email: str):
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)