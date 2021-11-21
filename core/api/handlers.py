from typing import Dict, List

from fastapi import APIRouter, Depends

from core.api.registry import ping_storage, user_storage, server_started, VERSION, ticket_storage
from core.model.ticket import Ticket
from core.model.user import User, UserRegisterRequest, Token, UserLoginRequest

router = APIRouter()


@router.get('/ping')
async def ping() -> Dict[str, str]:
    return {
        'ping': await ping_storage.ping(),
        'server_started': server_started,
        'version': VERSION
    }


@router.get('/api/user', response_model=User)
async def get_user(user: User = Depends(user_storage.get_user_by_token)):
    return user


@router.post('/api/register', response_model=Token)
async def register(register_request: UserRegisterRequest):
    user = await user_storage.add(first_name=register_request.first_name,
                                  second_name=register_request.second_name,
                                  middle_name=register_request.middle_name,
                                  login=register_request.login,
                                  password=register_request.password,
                                  passport=register_request.passport,
                                  role_id=register_request.role_id)
    token = user.get_token()
    return Token(access_token=token, token_type='bearer')


@router.post('/api/login', response_model=Token)
async def login(login_request: UserLoginRequest):
    user = await user_storage.get_user_by_login_password(login=login_request.login,
                                                         password=login_request.password)
    token = user.get_token()
    return Token(access_token=token, token_type='bearer')


@router.get('/api/users', response_model=str)
async def users() -> Dict[str, str]:
    return await ping_storage.get_value_hello()


@router.get('/api/tickets/feed', response_model=List[Ticket])
async def tickets_feed():
    return await ticket_storage.get_all_tickets()
