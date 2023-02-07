from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException, status

from ..db import get_db
from ..func import utils
from ..models import schemas
from ..models.models import User

# from ..models.schemas import UserLogin



SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(tags=['Authrntication'])


@router.post('/login')
def login(user_credential: schemas.UserLogin,db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email==user_credential.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")

    if not utils.verify_password(user_credential.password, user.password):
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials")

    return {"token": "token data"}




