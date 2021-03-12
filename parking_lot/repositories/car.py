import time
from mysql import connector
from parking_lot.db_conn.connection import DBConnection
from parking_lot.entities.car import Car


class CarRepository:
    def __init__(self):
        self.db = DBConnection.instance().connection

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
        finally:
            if self.db.is_connected():
                m_cursor.close()
        return car_id

    def clean_up(self):
        m_cursor = self.db.cursor()
        try:
            sql = "TRUNCATE TABLE vehicle;"
            m_cursor.execute(sql)
            self.db.commit()
        except connector.Error as e:
            print(e)
        finally:
            if self.db.is_connected():
                m_cursor.close()
