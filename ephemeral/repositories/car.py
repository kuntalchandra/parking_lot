import time
from typing import Dict

from mysql import connector
from parking_lot.db_conn.connection import DBConnection
from parking_lot.entities.car import Car
from parking_lot.helper.debug_helper import DebugHelper


class CarRepository:
    def __init__(self):
        self.db = DBConnection.instance().connection

    def get_car_partial(self, car_id: int) -> Dict:
        m_cursor = self.db.cursor()
        car = {}
        try:
            m_cursor.execute("SELECT id, in_at FROM vehicle WHERE id = {}".format(car_id))
            for row in m_cursor:
                car["id"] = row[0]
                car["in_at"] = row[1]
        except connector.Error as e:
            print(e)
            DebugHelper.print_exception()
        finally:
            if self.db.is_connected():
                m_cursor.close()
        return car

    def park(self, car: Car) -> int:
        m_cursor = self.db.cursor()
        now = time.strftime("%Y-%m-%d %H-%M-%S")
        car_id = None
        try:
            sql = "INSERT INTO vehicle (color, registration_no, in_at) VALUES (%s, %s, %s)"
            value = (car.get_color(), car.get_registration_number(), now)
            m_cursor.execute(sql, value)
            self.db.commit()
            car_id = m_cursor.lastrowid
        except connector.Error as e:
            print(e)
            DebugHelper.print_exception()
        finally:
            if self.db.is_connected():
                m_cursor.close()
        return car_id

    def vacate(self, car: Car) -> bool:
        m_cursor = self.db.cursor()
        try:
            now = time.strftime("%Y-%m-%d %H-%M-%S")
            sql = "UPDATE vehicle SET out_at = %s WHERE id = %s"
            value = (now, car.get_id())
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
            sql = "TRUNCATE TABLE vehicle;"
            m_cursor.execute(sql)
            self.db.commit()
        except connector.Error as e:
            print(e)
            DebugHelper.print_exception()
        finally:
            if self.db.is_connected():
                m_cursor.close()
