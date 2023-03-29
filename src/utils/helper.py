# Packages
import string
import random
from typing import Optional, Dict, Any, AnyStr
from jose import JWTError, jwt, ExpiredSignatureError
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from dataclasses import dataclass, field, asdict
from passlib.context import CryptContext
from dicttoxml import dicttoxml
from datetime import datetime, timedelta

# Modules
from config import AUTH_ALGORITHM, AUTH_SECRET_KEY
from utils.exceptions import JWTTokenError


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/sign-in")


@dataclass
class ReturnValue:
    status: bool = True
    http_code: Optional[int] = -1
    message: str = ""
    error: str = ""
    data: Any = field(default_factory=list)

    def to_dict(self) -> Dict:
        return asdict(self)


class Helper:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def dict_to_xml(data: Dict) -> AnyStr:
        return dicttoxml(data, attr_type=False)

    @staticmethod
    def generate_hased_password(password: str) -> AnyStr:
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(payload: Dict, secret_key: str, algo: str, expire: int = 15) -> AnyStr:
        to_encode = payload.copy()
        expire = datetime.utcnow() + timedelta(minutes=expire)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algo)
        return encoded_jwt

    @staticmethod
    def generate_random_text(l: int = 6) -> AnyStr:
        return ''.join(random.choices(string.ascii_uppercase +
                                      string.digits, k=l))

    @staticmethod
    def get_token_payload(token: str = Depends(oauth2_scheme)) -> Dict:
        try:
            payload = jwt.decode(token, AUTH_SECRET_KEY,
                                 algorithms=[AUTH_ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise JWTTokenError(
                    status.HTTP_401_UNAUTHORIZED, "Could not find user"
                )

            return payload

        except ExpiredSignatureError:
            raise JWTTokenError(
                status.HTTP_401_UNAUTHORIZED, "Token expired"
            )

        except JWTError:
            raise JWTTokenError(
                status.HTTP_401_UNAUTHORIZED, "Invalid token"
            )
