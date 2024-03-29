from typing import Optional, List

import bcrypt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from core.model.user import TokenData, User, SECRET_KEY, ALGORITHM, UserResponse
from core.storage.sql_server import DB
from core.utils.utils import throw_credential_exception, throw_not_found, throw_server_error, throw_bad_request

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

    async def get_user_by_login_password(self, login: str, password: str) -> User:
        sql = 'SELECT * FROM [User] WHERE (login_ = ?)'
        res = await self.db.execute(sql, login)
        if not res:
            throw_not_found('No user with this login and password!')
        user = User.parse_obj(res[0])
        if not bcrypt.checkpw(password.encode(), user.password_.encode()):
            throw_bad_request("Wrong password!")
        return user

    async def get_user_by_passport(self, passport: str) -> User:
        sql = 'SELECT * FROM [User] WHERE (passport = ?)'
        row = await self.db.execute(sql, passport)
        if not row:
            throw_not_found('No user with this passport!')
        user = User.parse_obj(row[0])
        return user

    async def get_user_by_id(self, user_id: int) -> User:
        sql = 'SELECT * FROM [User] WHERE (user_id = ?)'
        row = await self.db.execute(sql, user_id)
        if not row:
            throw_not_found('No user with this id!')
        user = User.parse_obj(row[0])
        return user

    async def get_all_users_by_role(self, role_id: int) -> List[User]:
        sql = 'SELECT * FROM [User] u WHERE (u.role_id = ?)'
        rows = await self.db.execute(sql, role_id)
        output: List[User] = []
        for row in rows:
            output.append(User.parse_obj(row))
        return output

    async def get_all_users(self) -> List[UserResponse]:
        sql = 'SELECT * FROM [User]'
        rows = await self.db.execute(sql)
        output: List[UserResponse] = []
        for row in rows:
            sql2 = 'SELECT COUNT(*) as count FROM [Order] WHERE user_id = ? AND is_canceled = 0'
            count_row = await self.db.execute(sql2, row['user_id'])
            output.append(UserResponse(
                **(User.parse_obj(row)).dict(),
                amount_of_orders=count_row[0]['count']
            ))
        output.sort(key=lambda u: u.amount_of_orders, reverse=True)
        return output

    async def add(self,
                  first_name: str,
                  second_name: str,
                  middle_name: Optional[str],
                  login: str,
                  password: str,
                  passport: str,
                  role_id: int) -> User:
        sql = 'INSERT INTO [User] (first_name,' \
              'second_name,' \
              'middle_name,' \
              'login_, ' \
              'password_,' \
              'passport, role_id) VALUES (?,?,?,?,?,?,?)'
        await self.db.execute(sql,
                              first_name,
                              second_name,
                              middle_name,
                              login,
                              password,
                              passport,
                              role_id)
        sql2 = 'SELECT * FROM [User] WHERE login_ = ? AND password_ = ?'
        row = await self.db.execute(sql2,
                                    login,
                                    password)
        if not row:
            throw_server_error('Unable to add to table User!')
        user = User.parse_obj(row[0])
        return user

    async def update(self, user: User) -> None:
        sql = 'UPDATE [User] SET first_name = ?,' \
              'second_name = ?,' \
              'middle_name = ?,' \
              'login_ = ?,' \
              'password_ = ?,' \
              'role_id = ? WHERE user_id = ?'
        await self.db.execute(sql,
                              user.first_name,
                              user.second_name,
                              user.middle_name,
                              user.login_,
                              user.password_,
                              user.role_id,
                              user.user_id)

    async def delete(self, user_id: int):
        sql = 'DELETE FROM [User] WHERE user_id = ?'
        await self.db.execute(sql, user_id)
