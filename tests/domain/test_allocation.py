from unittest import TestCase

from parking_lot.domain.allocation import (
    DefaultSpaceAllocationPolicy,
    SpaceAllocationPolicy,
)
from parking_lot.domain.models import (
    ParkingSpaceSize,
    VehicleSize,
)


class DefaultSpaceAllocationPolicyTest(TestCase):
    def setUp(self) -> None:
        self.policy = DefaultSpaceAllocationPolicy()

    def test_small_vehicle_prefers_small_then_medium_then_large(
        self,
    ) -> None:
        preferred_sizes = self.policy.preferred_space_sizes(
            VehicleSize.SMALL
        )

        self.assertTupleEqual(
            (
                ParkingSpaceSize.SMALL,
                ParkingSpaceSize.MEDIUM,
                ParkingSpaceSize.LARGE,
            ),
            preferred_sizes,
        )

    def test_default_policy_satisfies_policy_contract(self) -> None:
        policy: SpaceAllocationPolicy = self.policy

        self.assertIsInstance(
            policy,
            DefaultSpaceAllocationPolicy,
        )