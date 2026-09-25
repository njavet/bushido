from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from citadel.auth.tokens import decode_access_token
from citadel.persistence.models import Spartan


def get_session(request: Request) -> Generator[Session]:
    sf = request.app.state.sf
    with sf.session() as session:
        yield session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
Oauth2SchemeDep = Annotated[str, Depends(oauth2_scheme)]
SessionDep = Annotated[Session, Depends(get_session)]


def get_current_user(token: Oauth2SchemeDep, session: SessionDep) -> Spartan:
    try:
        user_id = decode_access_token(token)
    except Exception as e:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

    user = session.get(Spartan, user_id)
    if user is None or not user.is_active:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User not found or inactive")
    return user


UserDep = Annotated[Spartan, Depends(get_current_user)]
