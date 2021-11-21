from typing import Optional, List

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from core.model.user import TokenData, User, SECRET_KEY, ALGORITHM
from core.storage.sql_server import DB
from core.utils.utils import throw_credential_exception, throw_not_found, throw_server_error

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserStorage:

    def __init__(self, db: DB) -> None:
        self.db = db

    async def get_user_by_token(self, token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            passport: str = payload.get("sub")
            if passport is None:
                throw_credential_exception()
            token_data = TokenData(passport=passport)
        except JWTError:
            throw_credential_exception()
        user = await self.get_user_by_passport(passport=token_data.passport)
        if user is None:
            throw_credential_exception()
        return user

    async def get_user_by_passport(self, passport: str) -> User:
        sql = 'SELECT * FROM User WHERE (passport = $1)'
        row = await self.db.fetch_row(sql, passport)
        if not row:
            throw_not_found('No user with this passport!')
        user = User.parse_obj(row)
        return user

    async def get_user_by_id(self, user_id: int) -> User:
        sql = 'SELECT * FROM User WHERE (user_id = $1)'
        row = await self.db.fetch_row(sql, user_id)
        if not row:
            throw_not_found('No user with this id!')
        user = User.parse_obj(row)
        return user

    async def get_all_users_by_role(self, role_id: int) -> List[User]:
        sql = 'SELECT * FROM User u WHERE (u.role_id = $1)'
        rows = await self.db.fetch(sql, role_id)
        output: List[User] = []
        for row in rows:
            output.append(User.parse_obj(row))
        return output

    async def add(self,
                  first_name: str,
                  second_name: str,
                  middle_name: Optional[str],
                  passport: str,
                  role_id: int) -> User:
        sql = f'INSERT INTO User (' \
              'first_name,' \
              ' second_name,' \
              ' middle_name,' \
              ' passport, role_id,' \
              ' VALUES ($1,$2,$3,$4,$5) RETURNING *'
        row = await self.db.fetch_row(sql,
                                      first_name,
                                      second_name,
                                      middle_name,
                                      passport,
                                      role_id)
        if not row:
            throw_server_error('Unable to add to table User!')
        user = User.parse_obj(row)
        return user

    async def update(self, user: User) -> None:
        sql = 'UPDATE User SET (' \
              'first_name,' \
              'second_name,' \
              'middle_name,' \
              'passport,' \
              'role_id)= ($2,$3,$4,$5,$6) WHERE id = $1'
        await self.db.execute(sql,
                              user.user_id,
                              user.first_name,
                              user.second_name,
                              user.middle_name,
                              user.passport,
                              user.role_id)

    async def delete(self, user_id: int):
        sql = 'DELETE FROM User WHERE user_id = $1'
        await self.db.execute(sql, user_id)
