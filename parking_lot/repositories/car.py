import time
from parking_lot.db_conn.connection import DBConnection
from parking_lot.entities.car import Car


class CarRepository:
    def __init__(self):
        self.db = DBConnection.instance().connection

    def park(self, car: Car) -> int:
        m_cursor = self.db.cursor()
        now = time.strftime("%Y-%m-%d %H-%M-%S")
        sql = "INSERT INTO vehicle (color, registration_no, in_at) VALUES (%s, %s, %s)"
        value = (car.get_color(), car.get_registration_number(), now)
        m_cursor.execute(sql, value)
        self.db.commit()
        return self.db.insert_id()
