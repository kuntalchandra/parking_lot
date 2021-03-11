from parking_lot.db_conn.connection import DBConnection
from parking_lot.entities.car import Car
from parking_lot.entities.parking_slot import ParkingSlot


class ParkingSlotRepository:
    def __init__(self):
        self.db = DBConnection.instance().connection

    def reserve(self, slot: ParkingSlot, car: Car) -> int:
        m_cursor = self.db.cursor()
        sql = "INSERT INTO parking_slot (merchant_id, parking_lot_id, vehicle_id, available) VALUES (%s, %s, %s, %s)"
        value = (1, slot.parking_lot.id(), car.get_id(), "1")
        m_cursor.execute(sql, value)
        self.db.commit()
        return self.db.insert_id()
