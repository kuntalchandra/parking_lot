from unittest import TestCase

from parking_lot.exceptions import InvalidCommandException

from parking_lot.services.parking_lot import ParkingLotService


class ParkingLotServiceTest(TestCase):
    def setUp(self) -> None:
        self.slots = 10

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
        self.assertEqual(obj.park("park KA-01-HH-1234",  "White"), 1)

    def test_park_full(self):
        obj = ParkingLotService()
        obj.create_parking_lot(str(self.slots))
        for i in range(self.slots):
            obj.park("park KA-01-HH" + str(i),  "White")
        self.assertFalse(obj.park("park KA-01-HH-1234",  "White"))

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
        obj.park("park KA-01-HH-1234",  "White")
        try:
            obj.leave(str(2))
        except InvalidCommandException as e:
            print(e)
