from datetime import datetime, timedelta, timezone
from unittest import TestCase

from parking_lot.domain.exceptions import (
    InvalidParkingDurationError,
)
from parking_lot.domain.pricing import (
    FixedHourlyPricingPolicy,
)


class FixedHourlyPricingPolicyTest(TestCase):
    def setUp(self) -> None:
        self.policy = FixedHourlyPricingPolicy()
        self.parked_at = datetime(
            2026,
            9,
            21,
            10,
            0,
            tzinfo=timezone.utc,
        )

    def test_charges_minimum_one_hour(self) -> None:
        charge = self.policy.calculate(
            parked_at=self.parked_at,
            exited_at=self.parked_at,
            hourly_rate=10,
        )

        self.assertEqual(1, charge.billed_hours)
        self.assertEqual(10, charge.total_cost)

    def test_charges_exact_completed_hours(self) -> None:
        charge = self.policy.calculate(
            parked_at=self.parked_at,
            exited_at=self.parked_at + timedelta(hours=2),
            hourly_rate=10,
        )

        self.assertEqual(2, charge.billed_hours)
        self.assertEqual(20, charge.total_cost)

    def test_rounds_partial_hour_upwards(self) -> None:
        charge = self.policy.calculate(
            parked_at=self.parked_at,
            exited_at=(
                self.parked_at
                + timedelta(hours=1, seconds=1)
            ),
            hourly_rate=10,
        )

        self.assertEqual(2, charge.billed_hours)
        self.assertEqual(20, charge.total_cost)

    def test_rounds_duration_below_one_hour_to_one(self) -> None:
        charge = self.policy.calculate(
            parked_at=self.parked_at,
            exited_at=(
                self.parked_at + timedelta(minutes=20)
            ),
            hourly_rate=10,
        )

        self.assertEqual(1, charge.billed_hours)
        self.assertEqual(10, charge.total_cost)

    def test_rejects_exit_before_parking(self) -> None:
        with self.assertRaises(InvalidParkingDurationError):
            self.policy.calculate(
                parked_at=self.parked_at,
                exited_at=(
                    self.parked_at - timedelta(seconds=1)
                ),
                hourly_rate=10,
            )