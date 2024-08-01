from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreateSchema, UserResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/users", tags=["Users"])


# Create a new user
@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreateSchema, session: Session = Depends(get_db)
) -> UserResponse:
    user_model = User(
        name=user.name,
        email=user.email,
        hashed_password=pwd_context.hash(user.password),
    )
    session.add(user_model)
    session.commit()
    session.refresh(user_model)
    user_response = session.query(User).filter(User.email == user.email).first()
    return user_response
