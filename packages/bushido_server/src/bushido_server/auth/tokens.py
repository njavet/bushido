import datetime

import jwt
from dotenv import load_dotenv

load_dotenv()
# TODO fix
SECRET_KEY = (
    "TEST"  # os.environ["JWT_SECRET_KEY"]  # from Azure App Service config / Key Vault
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 1 week — tune to taste


def create_access_token(user_id: int) -> str:
    now = datetime.datetime.now(datetime.UTC)
    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return str(jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM))


def decode_access_token(token: str) -> int:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return int(payload["sub"])
