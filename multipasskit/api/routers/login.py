from fastapi import  APIRouter

from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from fastapi import Depends, HTTPException, status

from multipasskit.api.models import token
from multipasskit.api.auth import authenticate_user, create_access_token
from multipasskit.api.db import SessionDep
from multipasskit.api.config import settings

router = APIRouter(prefix='/login', tags=["login"])

@router.post("/token")
async def login_for_access_token(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> token.Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = authenticate_user(session=session, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return token.Token(access_token=access_token, token_type="bearer")