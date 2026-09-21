from parking_lot.domain.exceptions import (
    InvalidParkingLotConfigurationError,
    ParkingLotNotFoundError,
)
from parking_lot.domain.models import (
    ParkingLot,
    ParkingSpaceSize,
)
from parking_lot.repositories.parking_lots import (
    ParkingLotRepository,
)


class ParkingLotService:
    def __init__(
        self,
        repository: ParkingLotRepository,
    ) -> None:
        self.repository = repository

    def create_parking_lot(
        self,
        name: str,
        small_space_count: int,
        medium_space_count: int,
        large_space_count: int,
        hourly_rate: int,
    ) -> ParkingLot:
        normalised_name = name.strip()

        self._validate_configuration(
            name=normalised_name,
            small_space_count=small_space_count,
            medium_space_count=medium_space_count,
            large_space_count=large_space_count,
            hourly_rate=hourly_rate,
        )

        space_sizes = (
            [ParkingSpaceSize.SMALL] * small_space_count
            + [ParkingSpaceSize.MEDIUM] * medium_space_count
            + [ParkingSpaceSize.LARGE] * large_space_count
        )

        return self.repository.create(
            name=normalised_name,
            hourly_rate=hourly_rate,
            space_sizes=space_sizes,
        )

    def get_parking_lot(
        self,
        parking_lot_id: int,
    ) -> ParkingLot:
        parking_lot = self.repository.get(parking_lot_id)

        if parking_lot is None:
            raise ParkingLotNotFoundError(
                f"Parking lot {parking_lot_id} does not exist"
            )

        return parking_lot

    def list_parking_lots(self) -> list[ParkingLot]:
        return self.repository.list_all()

    @staticmethod
    def _validate_configuration(
        name: str,
        small_space_count: int,
        medium_space_count: int,
        large_space_count: int,
        hourly_rate: int,
    ) -> None:
        if not name:
            raise InvalidParkingLotConfigurationError(
                "Parking lot name cannot be blank"
            )

        space_counts = (
            small_space_count,
            medium_space_count,
            large_space_count,
        )

        if any(count < 0 for count in space_counts):
            raise InvalidParkingLotConfigurationError(
                "Parking-space counts cannot be negative"
            )

        if sum(space_counts) == 0:
            raise InvalidParkingLotConfigurationError(
                "At least one parking space is required"
            )

        if hourly_rate <= 0:
            raise InvalidParkingLotConfigurationError(
                "Hourly rate must be greater than zero"
            )