from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import get_db
from app.models.user import UserModel
from app.schemas.user import UserCreateSchema, UserResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/users", tags=["Users"])


# Create a new user
@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreateSchema, db: Session = Depends(get_db)
) -> UserResponse:
    user_model = UserModel(
        name=user.name,
        email=user.email,
        hashed_password=pwd_context.hash(user.password),
    )
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    user_response = db.query(UserModel).filter(UserModel.email == user.email).first()
    return user_response
