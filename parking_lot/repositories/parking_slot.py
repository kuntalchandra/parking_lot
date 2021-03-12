from mysql import connector
from parking_lot.db_conn.connection import DBConnection
from parking_lot.entities.car import Car
from parking_lot.entities.parking_slot import ParkingSlot


class ParkingSlotRepository:
    def __init__(self):
        self.db = DBConnection.instance().connection

    def reserve(self, slot: ParkingSlot, car: Car) -> int:
        m_cursor = self.db.cursor()
        slot_id = None
        try:
            sql = "INSERT INTO parking_slot (merchant_id, parking_lot_id, vehicle_id, available) " \
                  "VALUES (%s, %s, %s, %s)"
            value = (slot.get_merchant().get_id(), slot.get_parking_lot().get_id(), car.get_id(), "0")
            m_cursor.execute(sql, value)
            self.db.commit()
            slot_id = m_cursor.lastrowid
        except connector.Error as e:
            print(e)
        finally:
            if self.db.is_connected():
                m_cursor.close()
        return slot_id

    def clean_up(self):
        m_cursor = self.db.cursor()
        try:
            sql = "TRUNCATE TABLE parking_slot"
            m_cursor.execute(sql)
            self.db.commit()
        except connector.Error as e:
            print(e)
        finally:
            if self.db.is_connected():
                m_cursor.close()
