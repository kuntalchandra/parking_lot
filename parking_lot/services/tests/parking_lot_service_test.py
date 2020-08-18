from unittest import TestCase
from parking_lot.exceptions import InvalidCommandException
from parking_lot.services.parking_lot import ParkingLotService


class ParkingLotServiceTest(TestCase):
    def setUp(self) -> None:
        self.slots = 10
        self.cars = [
            ["KA-01-HH-1234", "White"],
            ["KA-01-HH-9999", "White"],
            ["KA-01-BB-0001", "Black"],
        ]

    def test_create_parking_lot(self):
        obj = ParkingLotService()
        self.assertEqual(obj.create_parking_lot(str(self.slots)), 10)

    def test_parking_lot_exists(self):
        obj = ParkingLotService()
        obj.create_parking_lot(str(self.slots))
        self.assertTrue(obj.parking_lot_exists())

    def test_parking_lot_does_not_exists(self):
        obj = ParkingLotService()
        self.assertFalse(obj.parking_lot_exists())

    def test_park(self):
        obj = ParkingLotService()
        obj.create_parking_lot(str(self.slots))
        self.assertEqual(obj.park("park KA-01-HH-1234", "White"), 1)

    def test_park_full(self):
        obj = ParkingLotService()
        obj.create_parking_lot(str(self.slots))
        for i in range(self.slots):
            obj.park("park KA-01-HH" + str(i), "White")
        self.assertFalse(obj.park("park KA-01-HH-1234", "White"))

    def test_invalid_leave_range(self):
        obj = ParkingLotService()
        obj.create_parking_lot(str(self.slots))
        try:
            obj.leave(str(15))
        except InvalidCommandException as e:
            print(e)

    def test_invalid_leave_slot(self):
        obj = ParkingLotService()
        obj.create_parking_lot(str(self.slots))
        obj.park("park KA-01-HH-1234", "White")
        try:
            obj.leave(str(2))
        except InvalidCommandException as e:
            print(e)

    def test_status(self):
        obj = ParkingLotService()
        obj.create_parking_lot(str(self.slots))
        for details in self.cars:
            registration_number, color = details
            obj.park(registration_number, color)
        self.assertListEqual(
            [
                ["1", "KA-01-HH-1234", "White"],
                ["2", "KA-01-HH-9999", "White"],
                ["3", "KA-01-BB-0001", "Black"],
            ],
            obj.status(),
        )

    def test_registration_numbers_for_cars_with_colour(self):
        obj = ParkingLotService()
        obj.create_parking_lot(str(self.slots))
        for details in self.cars:
            registration_number, color = details
            obj.park(registration_number, color)
        self.assertListEqual(
            ["KA-01-HH-1234", "KA-01-HH-9999"],
            obj.registration_numbers_for_cars_with_colour("White"),
        )

    def test_slot_numbers_for_cars_with_colour(self):
        obj = ParkingLotService()
        obj.create_parking_lot(str(self.slots))
        for details in self.cars:
            registration_number, color = details
            obj.park(registration_number, color)
        self.assertListEqual([1, 2], obj.slot_numbers_for_cars_with_colour("White"))

    def test_slot_number_for_registration_number(self):
        obj = ParkingLotService()
        obj.create_parking_lot(str(self.slots))
        obj.park("park KA-01-HH-1234", "White")
        self.assertEqual(
            1, obj.slot_number_for_registration_number("park KA-01-HH-1234")
        )
