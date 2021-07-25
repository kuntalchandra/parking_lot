from typing import Dict

from mysql import connector
from parking_lot.db_conn.connection import DBConnection
from parking_lot.entities.car import Car
from parking_lot.entities.parking_slot import ParkingSlot
from parking_lot.helper.debug_helper import DebugHelper


class ParkingSlotRepository:
    def __init__(self):
        self.db = DBConnection.instance().connection

    def get_slot_partial(self, slot_id: int) -> Dict:
        m_cursor = self.db.cursor()
        slot = {}
        try:
            m_cursor.execute("SELECT id, available FROM parking_slot WHERE id = {}".format(slot_id))
            for row in m_cursor:
                slot["id"] = row[0]
                slot["available"] = row[1]
        except connector.Error as e:
            print(e)
            DebugHelper.print_exception()
        finally:
            if self.db.is_connected():
                m_cursor.close()
        return slot

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
            DebugHelper.print_exception()
        finally:
            if self.db.is_connected():
                m_cursor.close()
        return slot_id

    def vacate(self, slot: ParkingSlot) -> bool:
        m_cursor = self.db.cursor()
        try:
            sql = "UPDATE parking_slot SET available = %s WHERE id = %s"
            value = ('1', slot.get_id())
            m_cursor.execute(sql, value)
            self.db.commit()
        except connector.Error as e:
            print(e)
            DebugHelper.print_exception()
            return False
        finally:
            if self.db.is_connected():
                m_cursor.close()
        return True

    def clean_up(self):
        m_cursor = self.db.cursor()
        try:
            sql = "TRUNCATE TABLE parking_slot"
            m_cursor.execute(sql)
            self.db.commit()
        except connector.Error as e:
            print(e)
            DebugHelper.print_exception()
        finally:
            if self.db.is_connected():
                m_cursor.close()
