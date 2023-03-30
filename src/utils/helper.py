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
    """ReturnValue class is responsible for holding returned value from operations

    Args:
        success: True if operation is successful otherwise False
        http_code: http status code
        message: message after successful operation
        error: error message after failed operation
        data: resulted data after operation completion
    """
    status: bool = True
    http_code: Optional[int] = -1
    message: str = ""
    error: str = ""
    data: Any = field(default_factory=list)

    def to_dict(self) -> Dict:
        return asdict(self)


class Helper:
    @staticmethod
    def verify_password(
        plain_password: str,
        hashed_password: str
    ) -> bool:
        """Match plain password with hashed password

        Args:
            plain_password: plain string of password 
            hashed_password: hashed string of password

        Returns:
            True if passwords matched otherwise False
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def dict_to_xml(data: Dict) -> AnyStr:
        """Converts dict object into xml string

        Args:
            data: dict object

        Returns:
            XML format string
        """
        return dicttoxml(data, attr_type=False)

    @staticmethod
    def generate_hased_password(password: str) -> AnyStr:
        """Generate hashed password

        Args:
            password: plain string of password

        Returns:
            String of password in hashed format
        """
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(
        payload: Dict,
        secret_key: str,
        algo: str,
        expire: int = 15
    ) -> AnyStr:
        """Create jwt access token

        Args:
            payload: payload of token
            secret_key: secret key 
            algo: name of algorith
            expire: expiration time in minutes. Defaults to 15.

        Returns:
            Encoded string of jwt token
        """
        to_encode = payload.copy()
        expire = datetime.utcnow() + timedelta(minutes=expire)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algo)
        return encoded_jwt

    @staticmethod
    def generate_random_text(l: int = 6) -> AnyStr:
        """Generate random alphanumeric string

        Args:
            l: length of string. Defaults to 6.

        Returns:
            random string
        """
        return ''.join(random.choices(string.ascii_letters +
                                      string.digits, k=l))

    @staticmethod
    def get_token_payload(
        token: str = Depends(oauth2_scheme)
    ) -> Dict:
        """Decode jwt token and extract payload

        Args:
            token: encoded jwt token string. Defaults to Depends(oauth2_scheme).

        Raises:
            JWTTokenError: Any jwt related error

        Returns:
            payload of token
        """
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
