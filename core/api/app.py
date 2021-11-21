import logging
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.api.registry import db
import core.api.handlers as handlers

app = FastAPI()
app.include_router(handlers.router)

origins = [
    "http://localhost",
    "http://localhost:18300",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    await db.connect()
    logging.info("Server started")


@app.on_event("shutdown")
async def shutdown_event():
    await db.close()
    logging.info("Server shutting down")
