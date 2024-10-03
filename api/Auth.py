from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated, Dict
from datetime import datetime, timezone, timedelta
from decouple import config
from sqlalchemy.orm import Session
from jwt import InvalidTokenError
import jwt

from config.db import get_db
from schemas import SurveySchemas
from models import SurveyModels

router = APIRouter()

oauth_schema = OAuth2PasswordBearer(tokenUrl="/token")
SECRET_KEY = config("SECRET_KEY")
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def get_respondent(email: str, db: Session) -> SurveySchemas.Respondent | None:
    return db.query(SurveyModels.Respondent).filter(SurveyModels.Respondent.email == email).first()


def authenticate_respondent(email: str, db) -> SurveySchemas.Respondent | bool:
    respondent = get_respondent(email, db)
    if not respondent:
        return False

    return respondent


def get_current_user(token: Annotated[str, Depends(oauth_schema)],
                     db: Session = Depends(get_db)) -> SurveySchemas.Respondent:
    """
    Retrieves the current user based on the provided JWT token.

    This function decodes the JWT token to extract the email, then fetches
    the corresponding respondent from the database. If the token is invalid or
    the respondent does not exist, an HTTP 404 exception is raised.

    :param db: The database session.
    :param token: The JWT token provided by the user.
    :type token: Annotated[str, Depends(oauth_schema)]
    :return: The respondent associated with the token.
    :rtype: Respondent
    :raises HTTPException: If the token is invalid or the respondent is not found.
    """

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = {"email": email}
    except InvalidTokenError:
        raise credentials_exception

    respondent = get_respondent(token_data["email"], db)
    if respondent is None:
        raise HTTPException(
            status_code=404,
            detail="Respondent not found",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return respondent


@router.post("/token")
def authenticate(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)) -> Dict[
    str, str]:
    respondent = authenticate_respondent(form_data.username, db)
    if not respondent:
        raise HTTPException(
            status_code=404,
            detail="Respondent not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(days=7)
    token = create_access_token(
        data={"sub": respondent.email}, expires_delta=access_token_expires
    )

    return {"access_token": token, "token_type": "bearer"}
