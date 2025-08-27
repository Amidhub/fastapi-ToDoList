from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas
from argon2 import PasswordHasher


ph = PasswordHasher()


async def get_user_by_email(db: AsyncSession, email: str):
    q = select(models.User).where(models.User.email == email)
    res = await db.execute(q)
    return res.scalars().first()


async def create_user(db: AsyncSession, user_in: schemas.UserCreate):
    hashed = ph.hash(user_in.password)
    db_user = models.User(email=user_in.email, hashed_password=hashed)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def create_task(db: AsyncSession, owner_id: int, task_in: schemas.TaskCreate):
    task = models.Task(title=task_in.title, description=task_in.description, owner_id=owner_id)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def list_tasks(db: AsyncSession, owner_id: int):
    q = select(models.Task).where(models.Task.owner_id == owner_id)
    res = await db.execute(q)
    return res.scalars().all()


async def verify_password(hash: str, plain: str) -> bool:
    try:
        return ph.verify(hash, plain)
    except Exception:
        return False