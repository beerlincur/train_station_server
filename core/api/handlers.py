import json
from enum import Enum
from typing import Dict, List

from fastapi import APIRouter

from core.api.registry import ping_storage, user_storage, server_started, VERSION
from core.storage.ping_storage import Hello

router = APIRouter()


@router.get('/ping')
async def ping() -> Dict[str, str]:
    return {
        'ping': await ping_storage.ping(),
        'server_started': server_started,
        'version': VERSION
    }


@router.get('/users', response_model=str)
async def users() -> Dict[str, str]:
    return await ping_storage.get_value_hello()


@router.get('/tickets/feed', response_model=List[Ticket])
async def tickets_feed() -> Dict[str, str]:
    return await ping_storage.get_value_hello()
