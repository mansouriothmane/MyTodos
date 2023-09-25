import jwt

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.config import settings
from app.database import get_db
from app.models.user import UserModel
from app.schemas.auth import LoginSchema, TokenSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/token", tags=["Authentication"])


# Request for authentication token
@router.post("/", response_model=TokenSchema)
async def authenticate(
    login: LoginSchema, db: Session = Depends(get_db)
) -> TokenSchema:
    user = db.query(UserModel).filter(UserModel.email == login.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found",
        )
    if not user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incorrect password",
        )
    if not pwd_context.verify(secret=login.password, hash=user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Incorrect password",
        )
    # Create access token
    payload = {"name": user.name, "sub": str(user.id)}
    access_token = jwt.encode(payload, settings.TOKEN_KEY)
    return TokenSchema(access_token=access_token, token_type="bearer")
