from typing import Dict, List

from fastapi import APIRouter, Depends

from core.api.registry import ping_storage, user_storage, server_started, VERSION, ticket_storage, race_storage, \
    order_storage, road_storage, station_storage, train_storage, road_station_storage
from core.helpers.ticket import generate_tickets_response, generate_ticket_response
from core.model.order import OrderResponse, OrderCreateRequest, OrderCancelRequest
from core.model.race import RaceResponse, RaceConductorResponse
from core.model.road import RoadResponse, RoadCreateRequest
from core.model.road_station import RoadStationCreateRequest, RoadStationRaceResponse
from core.model.station import Station, StationCreateRequest
from core.model.ticket import TicketResponse, TicketSetInTrainRequest, TicketCreateRequest
from core.model.train import Train, TrainCreateRequest, TrainResponse
from core.model.user import User, UserRegisterRequest, Token, UserLoginRequest, UserUpdateRequest, Role, UserResponse

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


@router.get('/api/tickets/all', response_model=List[TicketResponse])
async def tickets_feed(user: User = Depends(user_storage.get_user_by_token)):
    tickets = await ticket_storage.get_all_tickets()
    return await generate_tickets_response(tickets)


@router.get('/api/races/all', response_model=List[RaceResponse])
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


@router.put('/api/ticket/set_is_in_train', response_model=List[RaceConductorResponse])
async def set_ticket_is_in_train(ticket_request: TicketSetInTrainRequest,
                                 user: User = Depends(user_storage.get_user_by_token)):
    await ticket_storage.set_is_in_train(ticket_request.is_in_train, ticket_request.ticket_id)
    return await race_storage.get_races_by_conductor(user.user_id)


@router.post('/api/ticket/create', response_model=List[TicketResponse])
async def create_ticket(ticket_request: TicketCreateRequest, user: User = Depends(user_storage.get_user_by_token)):
    await ticket_storage.create(
        road_id=ticket_request.road_id,
        departure_station_id=ticket_request.departure_station_id,
        arrival_station_id=ticket_request.arrival_station_id,
        car_number=ticket_request.car_number,
        seat_number=ticket_request.seat_number,
        race_number=ticket_request.race_number
    )
    tickets = await ticket_storage.get_by_race_id(ticket_request.race_number)
    return await generate_tickets_response(tickets)


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


@router.get('/api/roads/all', response_model=List[RoadResponse])
async def roads_all(user: User = Depends(user_storage.get_user_by_token)):
    return await road_storage.get_all()


@router.post('/api/road/create', response_model=List[RoadResponse])
async def create_road(road_request: RoadCreateRequest, user: User = Depends(user_storage.get_user_by_token)):
    await road_storage.create(road_request.name)
    return await road_storage.get_all()


@router.get('/api/stations/all', response_model=List[Station])
async def stations_all(user: User = Depends(user_storage.get_user_by_token)):
    return await station_storage.get_all()


@router.post('/api/station/create', response_model=List[Station])
async def create_station(station_request: StationCreateRequest, user: User = Depends(user_storage.get_user_by_token)):
    await station_storage.create(station_request.name)
    return await station_storage.get_all()


@router.get('/api/conductors/all', response_model=List[User])
async def conductors_all(user: User = Depends(user_storage.get_user_by_token)):
    return await user_storage.get_all_users_by_role(Role.conductor)


@router.get('/api/users/all', response_model=List[UserResponse])
async def users_all(user: User = Depends(user_storage.get_user_by_token)):
    return await user_storage.get_all_users()


@router.get('/api/trains/all', response_model=List[TrainResponse])
async def trains_all(user: User = Depends(user_storage.get_user_by_token)):
    return await train_storage.get_all()


@router.post('/api/train/create', response_model=List[Train])
async def create_train(train_request: TrainCreateRequest,
                       user: User = Depends(user_storage.get_user_by_token)):
    await train_storage.create(train_request.name)
    return await train_storage.get_all()


@router.post('/api/road_station/create', response_model=List[RaceResponse])
async def create_road_station(road_station_request: RoadStationCreateRequest,
                              user: User = Depends(user_storage.get_user_by_token)):
    await road_station_storage.create(road_station_request)
    return await race_storage.get_all_future_races()


@router.get('/api/race/road_stations')
async def road_stations_by_race(race_number: int, user: User = Depends(user_storage.get_user_by_token)):
    return {
        "road_stations": await road_station_storage.get_by_race(race_number),
        "road_id": await road_storage.get_id_by_race_number(race_number)
    }
