from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import User, Role
from .utils import get_password_hash
from src.settings import settings
import logging

logger = logging.getLogger(__name__)

async def create_admin_user(session: AsyncSession):
    result = await session.execute(select(User).where(User.email == settings.ADMIN_EMAIL))
    admin = result.scalar_one_or_none()

    if admin:
        logger.info("Admin user already exists.")
        return

    admin_user = User(
        username=settings.ADMIN_USERNAME,
        email=settings.ADMIN_EMAIL,
        hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
        role=Role.ADMIN,
        disabled=False,
        balance=0.0
    )

    session.add(admin_user)
    await session.commit()
    logger.info("Admin user successfully created.")