from collections.abc import AsyncGenerator

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.security import decode_access_token
from app.database import AsyncSessionLocal
from app.models import User, UserRole


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

#tells fastAPI where the login route is
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

#passes the token to extract the user from the JWT token
async def get_current_user(token: str = Depends(oauth2_scheme),db: AsyncSession = Depends(get_db),) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = decode_access_token(token)

        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception

    #checks the database for the most updated set of Users
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    #checks if the user is still active
    if not user.is_active:
       raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Inactive user"
        )
    return user

#check if a user has persmissions to access a particular route
def require_role(*allowed_roles: UserRole):
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"Role '{current_user.role.value}' is not permitted to perform this action"
                ),
            )
        return current_user
    return role_checker