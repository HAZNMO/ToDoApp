from typing import Annotated
from typing import Any

import jwt
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from passlib.context import CryptContext

from to_do_app.API.utils.datetime import utcnow
from to_do_app.API.utils.token_expire import token_expire
from to_do_app.core.config import settings
from to_do_app.dependencies.auth.schemas import TokenModel

security = HTTPBearer()
security_dependency = Depends(security)

JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = settings.JWT_ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Функция создания JWT токена
# TODO pass user as argument and make token on user base
def create_token(user_id: str, email: str) -> str:
    expiration = token_expire()

    token_data = TokenModel(
        user_id=user_id,
        email=email,
        exp=expiration,
        timestamp=utcnow().isoformat(),
    )

    payload = token_data.model_dump(by_alias=True)
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


# Функция декодирования JWT токена
def decode_token(
    credentials: HTTPAuthorizationCredentials = security_dependency,
) -> dict:
    token = credentials.credentials
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError as err:
        raise HTTPException(status_code=401, detail="Token has expired") from err
    except jwt.InvalidTokenError as err:
        raise HTTPException(status_code=401, detail="Invalid token") from err
    else:
        return decoded


def get_user_id(
    decoded_context: Annotated[dict[str, Any], Depends(decode_token)]
) -> str:
    return decoded_context.get("user_id")
