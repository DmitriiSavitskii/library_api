from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.database import SessionDepends
from app.schemas.users import UserCreate, UserLogin, Token
from app.models.users import User
from app.core.security import hash_password, create_access_token
from app.core.security import verify_password


router = APIRouter()


@router.post("/register", response_model=Token)
async def register(user_create: UserCreate, session: SessionDepends):
    query = await session.execute(
        select(User).where(User.email == user_create.email))
    existing_user = query.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user_create.password)
    new_user = User(email=user_create.email, hashed_password=hashed_pw)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    token = create_access_token(data={"sub": new_user.email})
    return Token(access_token=token)


@router.post("/login", response_model=Token)
async def login(user_login: UserLogin, session: SessionDepends):
    query = await session.execute(
        select(User).where(User.email == user_login.email))
    user = query.scalars().first()

    if not user or not verify_password(
        user_login.password,
        user.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": user.email})
    return Token(access_token=token)
