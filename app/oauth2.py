from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from app.db_models import User
from app.schemas import TokenData
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.utils import verify_password
from app.database import SessionLocal
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.user_id==user_id).first()

    if not user:
        return None
    
    return user


def authenticate_user(db: Session, email: str, password: str):

    user = db.query(User).filter(User.email==email).first()

    if not user:
        return False
    
    if not verify_password(password,user.password):
        return False
    
    return user



def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id:  int = payload.get("id")
      
        if username is None:
            raise credentials_exception
        
        if user_id is None:
            raise credentials_exception
        
        token_data = TokenData(user_id=user_id,username=username)
    except JWTError:
        raise credentials_exception
    db = SessionLocal()
    user = get_user(db=db,user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user