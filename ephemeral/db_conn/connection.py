from mysql import connector
from mysql.connector import errorcode
from parking_lot.db_conn.singleton import Singleton


@Singleton
class DBConnection(object):
    def __init__(self):
        try:
            self.connection = connector.connect(host='localhost', user='root', password='', database='parking_lot')
        except connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with the user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            self.connection.close()
