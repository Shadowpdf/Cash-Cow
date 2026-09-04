import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt


SECRET_KEY = os.environ.get("SECRET_KEY", "<replace with a real key>")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#create credential
def hash_password(plain_password: str) -> str:
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")

#check credential
def verify_password(plain_password: str, hashed_password: str) ->bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

#issue identity
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    #to_encode is a copy of the input data dictionary, which will be used to create the payload of JWT
    to_encode = data.copy()

    #check if an expiration time provided; if not, we can use the default expiration time defined by
    #ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#verify identity
def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])