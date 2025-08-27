from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app import schemas, requests
from app.auth import auth


router = APIRouter()


@router.post("/register")
async def register(user_in: schemas.UserCreate, db: AsyncSession = Depends(get_db)
                   ) -> schemas.UserOut:
    exists = await requests.get_user_by_email(db, user_in.email)
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await requests.create_user(db, user_in)
    return user


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
                ) -> schemas.Token:
    user = await requests.get_user_by_email(db, form_data.username)
    if not user or not await requests.verify_password(user.hashed_password, form_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    token = auth.create_access_token(subject=str(user.email))
    return {"access_token": token, "token_type": "bearer"}


@router.post("/tasks")
async def create_task(task_in: schemas.TaskCreate, db: AsyncSession = Depends(get_db), subject: str = Depends(auth.get_current_subject)
                      ) -> schemas.TaskOut:
    user = await requests.get_user_by_email(db, subject)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await requests.create_task(db, user.id, task_in)


@router.get("/tasks")
async def list_tasks(db: AsyncSession = Depends(get_db), subject: str = Depends(auth.get_current_subject)
                     ) -> list[schemas.TaskOut]:
    user = await requests.get_user_by_email(db, subject)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await requests.list_tasks(db, user.id)