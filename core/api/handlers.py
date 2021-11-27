from typing import Dict, List

from fastapi import APIRouter, Depends

from core.api.registry import ping_storage, user_storage, server_started, VERSION, ticket_storage, race_storage, \
    order_storage, road_storage
from core.helpers.ticket import generate_tickets_response, generate_ticket_response
from core.model.order import OrderResponse, OrderCreateRequest, OrderCancelRequest
from core.model.race import RaceResponse, RaceConductorResponse
from core.model.road import RoadResponse
from core.model.ticket import TicketResponse
from core.model.user import User, UserRegisterRequest, Token, UserLoginRequest, UserUpdateRequest

import bcrypt

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
                                  password=bcrypt.hashpw(register_request.password.encode(), bcrypt.gensalt()),
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


@router.put('/api/user', response_model=User)
async def update_user(user_id: int, user_request: UserUpdateRequest,
                      user: User = Depends(user_storage.get_user_by_token)):
    user_output = await user_storage.get_user_by_id(user_id)
    user_request.update_user(user_output)
    await user_storage.update(user_output)
    return user_output


@router.get('/api/tickets/feed', response_model=List[TicketResponse])
async def tickets_feed(user: User = Depends(user_storage.get_user_by_token)):
    tickets = await ticket_storage.get_all_tickets()
    return await generate_tickets_response(tickets)


@router.get('/api/races/feed', response_model=List[RaceResponse])
async def races_feed(user: User = Depends(user_storage.get_user_by_token)):
    return await race_storage.get_all_future_races()


@router.get('/api/races/conductor', response_model=List[RaceConductorResponse])
async def races_by_conductor(user: User = Depends(user_storage.get_user_by_token)):
    return await race_storage.get_races_by_conductor(user.user_id)


@router.get('/api/road/races', response_model=List[RaceResponse])
async def races_by_road(road_id: int, user: User = Depends(user_storage.get_user_by_token)):
    return await race_storage.get_races_by_road(road_id)


@router.get('/api/tickets', response_model=List[TicketResponse])
async def tickets_by_race(race_id: int, user: User = Depends(user_storage.get_user_by_token)):
    tickets = await ticket_storage.get_by_race_id(race_id)
    return await generate_tickets_response(tickets)


@router.post('/api/order/create', response_model=List[OrderResponse])
async def create_order(order_request: OrderCreateRequest, user: User = Depends(user_storage.get_user_by_token)):
    await order_storage.create(user.user_id, order_request.ticket_id)
    orders = await order_storage.get_by_user_id(user.user_id)
    output = []
    for order in orders:
        output.append(
            OrderResponse(
                order_id=order.order_id,
                user_id=order.user_id,
                ticket=await generate_ticket_response(order.ticket_id, None),
                created_at=order.created_at,
                is_canceled=order.is_canceled
            )
        )
    return output


@router.put('/api/order/cancel', response_model=List[OrderResponse])
async def cancel_order(order_request: OrderCancelRequest, user: User = Depends(user_storage.get_user_by_token)):
    await order_storage.cancel(order_request.order_id)
    orders = await order_storage.get_by_user_id(user.user_id)
    output = []
    for order in orders:
        output.append(
            OrderResponse(
                order_id=order.order_id,
                user_id=order.user_id,
                ticket=await generate_ticket_response(order.ticket_id, None),
                created_at=order.created_at,
                is_canceled=order.is_canceled
            )
        )
    return output


@router.get('/api/orders', response_model=List[OrderResponse])
async def get_orders(user: User = Depends(user_storage.get_user_by_token)):
    orders = await order_storage.get_by_user_id(user.user_id)
    output = []
    for order in orders:
        output.append(
            OrderResponse(
                order_id=order.order_id,
                user_id=order.user_id,
                ticket=await generate_ticket_response(order.ticket_id, None),
                created_at=order.created_at,
                is_canceled=order.is_canceled
            )
        )
    return output


@router.get('/api/roads/feed', response_model=List[RoadResponse])
async def roads_feed(user: User = Depends(user_storage.get_user_by_token)):
    return await road_storage.get_all()



