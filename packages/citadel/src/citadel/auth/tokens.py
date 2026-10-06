import datetime

import jwt

from citadel.conf import settings


def create_access_token(user_id: int) -> str:
    now = datetime.datetime.now(datetime.UTC)
    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now
        + datetime.timedelta(minutes=settings.jwt_access_token_expire_minutes),
    }
    return jwt.encode(
        payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )


def decode_access_token(token: str) -> int:
    payload = jwt.decode(
        token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
    )
    return int(payload["sub"])
