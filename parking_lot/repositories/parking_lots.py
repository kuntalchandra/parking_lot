from typing import List, Dict
from mysql import connector
from parking_lot.db_conn.connection import DBConnection
from parking_lot.helper.debug_helper import DebugHelper


class ParkingLotRepository:
    def __init__(self):
        self.db = DBConnection.instance().connection

    def get_all(self) -> List[Dict]:
        m_cursor = self.db.cursor()
        lots = []
        try:
            m_cursor.execute("SELECT * FROM parking_lot WHERE is_available = '1'")
            rs = m_cursor.fetchall()
            for x in rs:
                lot = dict()
                lot["id"] = x[0]
                lot["name"] = x[1]
                lot["location"] = x[2]
                lot["pin"] = x[3]
                lot["size"] = x[6]
                lots.append(lot)
        except connector.Error as e:
            print(e)
            DebugHelper.print_exception()
        finally:
            if self.db.is_connected():
                m_cursor.close()
        return lots

    def get_lot(self, slot_id: int) -> Dict:
        m_cursor = self.db.cursor()
        lot = {}
        try:
            m_cursor.execute("SELECT * FROM parking_lot WHERE id = {}".format(slot_id))
            for row in m_cursor:
                lot["id"] = row[0]
                lot["name"] = row[1]
                lot["location"] = row[2]
                lot["pin"] = row[3]
                lot["size"] = row[6]
        except connector.Error as e:
            print(e)
            DebugHelper.print_exception()
        finally:
            if self.db.is_connected():
                m_cursor.close()
        return lot

