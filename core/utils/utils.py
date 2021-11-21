import logging
import multiprocessing
import os
import ssl

from fastapi import HTTPException
from starlette import status


def on_process_start():
    ssl._create_default_https_context = ssl._create_unverified_context
    process_name = multiprocessing.current_process().name
    logger = logging.getLogger()
    logger.name = process_name
    logger.setLevel(level=logging.INFO)
    logging.info(f'Process {process_name} started')
    for k, v in os.environ.items():
        logging.info(f'{k}={v}')


def throw_server_error(message: str):
    raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, message)


def throw_bad_request(message: str):
    raise HTTPException(status.HTTP_400_BAD_REQUEST, message)


def throw_not_found(message: str):
    raise HTTPException(status.HTTP_404_NOT_FOUND, message)


def throw_credential_exception():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
