from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from parking_lot.domain.exceptions import (
    InvalidParkingLotConfigurationError,
    ParkingLotAlreadyExistsError,
    ParkingLotNotFoundError,
)


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(
        InvalidParkingLotConfigurationError
    )
    async def invalid_configuration_handler(
        request: Request,
        exception: InvalidParkingLotConfigurationError,
    ) -> JSONResponse:
        return _error_response(
            status_code=422,
            code="INVALID_PARKING_LOT_CONFIGURATION",
            message=str(exception),
        )

    @app.exception_handler(ParkingLotAlreadyExistsError)
    async def parking_lot_exists_handler(
        request: Request,
        exception: ParkingLotAlreadyExistsError,
    ) -> JSONResponse:
        return _error_response(
            status_code=409,
            code="PARKING_LOT_ALREADY_EXISTS",
            message=str(exception),
        )

    @app.exception_handler(ParkingLotNotFoundError)
    async def parking_lot_not_found_handler(
        request: Request,
        exception: ParkingLotNotFoundError,
    ) -> JSONResponse:
        return _error_response(
            status_code=404,
            code="PARKING_LOT_NOT_FOUND",
            message=str(exception),
        )


def _error_response(
    status_code: int,
    code: str,
    message: str,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": code,
                "message": message,
            }
        },
    )