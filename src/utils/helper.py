# Packages
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from dataclasses import dataclass, field, asdict
from passlib.context import CryptContext
from dicttoxml import dicttoxml
from datetime import datetime, timedelta


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass
class ReturnValue:
    status: bool = True
    http_code: Optional[int] = -1
    message: str = ""
    error: str = ""
    data: Any = field(default_factory=list)

    def to_dict(self):
        return asdict(self)


class Helper:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def dict_to_xml(data: Dict):
        return dicttoxml(data, attr_type=False)

    @staticmethod
    def generate_hased_password(password: str):
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(payload: Dict, secret_key: str, algo: str, expire: int = 15):
        to_encode = payload.copy()
        expire = datetime.utcnow() + timedelta(minutes=expire)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algo)
        return encoded_jwt
