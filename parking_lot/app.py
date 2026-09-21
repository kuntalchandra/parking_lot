from pathlib import Path

from fastapi import FastAPI

from parking_lot.api.errors import register_error_handlers
from parking_lot.api.parking_lots import router
from parking_lot.database import DEFAULT_DATABASE_PATH
from parking_lot.api.tickets import router as tickets_router
from parking_lot.api.parking_spaces import (
    router as parking_spaces_router,
)


def create_app(
    database_path: str | Path = DEFAULT_DATABASE_PATH,
) -> FastAPI:
    application = FastAPI(
        title="Parking Lot API",
        version="2.0.0",
    )
    application.state.database_path = database_path
    application.include_router(router)
    application.include_router(tickets_router)
    application.include_router(parking_spaces_router)
    register_error_handlers(application)
    return application


app = create_app()