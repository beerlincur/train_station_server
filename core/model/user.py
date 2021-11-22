from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from pydantic import BaseModel

ACCESS_TOKEN_EXPIRE_DAYS = 365
SECRET_KEY = "3BpwSDvq1YB5IJVSWi7AT1EaB8FchZSF6ShOG9C87CjxhsQiLS6S0CyWMiVIEuiw"
ALGORITHM = "HS256"


def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


class UserRegisterRequest(BaseModel):
    first_name: str
    second_name: str
    middle_name: Optional[str]
    login: str
    password: str
    passport: str
    role_id: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    passport: Optional[str] = None


class User(BaseModel):
    user_id: int
    first_name: str
    second_name: str
    middle_name: Optional[str]
    login_: str
    password_: str
    passport: str
    role_id: int

    def get_token(self) -> str:
        started_at = datetime.utcnow()
        token_expires = started_at + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
        token = create_access_token(
            data={"sub": self.passport, "exp": token_expires}
        )
        return token

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)


class UserLoginRequest(BaseModel):
    login: str
    password: str


class UserUpdateRequest(BaseModel):
    first_name: Optional[str]
    second_name: Optional[str]
    middle_name: Optional[str]
    login: Optional[str]
    password: Optional[str]

    def update_user(self, user: User) -> None:
        if self.first_name:
            user.first_name = self.first_name
        if self.second_name:
            user.second_name = self.second_name
        if self.middle_name:
            user.middle_name = self.middle_name
        if self.login:
            user.login_ = self.login
        if self.password:
            user.password_ = self.password
