from typing import Protocol

from parking_lot.domain.models import (
    ParkingSpaceSize,
    VehicleSize,
)


class SpaceAllocationPolicy(Protocol):
    def preferred_space_sizes(
        self,
        vehicle_size: VehicleSize,
    ) -> tuple[ParkingSpaceSize, ...]:
        """Return compatible space sizes in allocation priority order."""
        ...


class DefaultSpaceAllocationPolicy:
    def preferred_space_sizes(
        self,
        vehicle_size: VehicleSize,
    ) -> tuple[ParkingSpaceSize, ...]:
        """Return compatible spaces for the currently supported vehicle."""

        if vehicle_size is VehicleSize.SMALL:
            return (
                ParkingSpaceSize.SMALL,
                ParkingSpaceSize.MEDIUM,
                ParkingSpaceSize.LARGE,
            )

        raise ValueError(
            f"Unsupported vehicle size: {vehicle_size}"
        )