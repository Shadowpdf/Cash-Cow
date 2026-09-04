"""

"""


from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.models import User, UserRole
from app.schemas.user import Token, UserCreate, UserRead
from app.security import create_access_token, hash_password, verify_password


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token", response_model=Token)

#OAuth2PasswordRequestForm is used to extract the username and password from the body
async def login(form_data: OAuth2PasswordRequestForm = Depends(),db: AsyncSession = Depends(get_db),) -> Token:

    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()

    # checks to see if account is active
    if user is not None and not user.is_active:
        raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Inactive user"
        )

    #checking for correct password

    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    #set the access token/JWT
    access_token = create_access_token(data={"sub": user.username, "role": user.role.value})
    return Token(access_token=access_token, token_type="bearer")
