from dataclasses import dataclass
from datetime import datetime
from math import ceil
from typing import Protocol

from parking_lot.domain.exceptions import (
    InvalidParkingDurationError,
)


@dataclass(frozen=True, slots=True)
class ParkingCharge:
    billed_hours: int
    total_cost: int


class PricingPolicy(Protocol):
    def calculate(
        self,
        parked_at: datetime,
        exited_at: datetime,
        hourly_rate: int,
    ) -> ParkingCharge:
        ...


class FixedHourlyPricingPolicy:
    def calculate(
        self,
        parked_at: datetime,
        exited_at: datetime,
        hourly_rate: int,
    ) -> ParkingCharge:
        duration_seconds = (
            exited_at - parked_at
        ).total_seconds()

        if duration_seconds < 0:
            raise InvalidParkingDurationError(
                "Exit time cannot precede parking time"
            )

        billed_hours = max(
            1,
            ceil(duration_seconds / 3600),
        )

        return ParkingCharge(
            billed_hours=billed_hours,
            total_cost=billed_hours * hourly_rate,
        )