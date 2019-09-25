import psycopg2

from Launch_parameters import parameters

TABLE_NAME = "user_control"
ACCESS_TIME = 300
ACCESS_COUNT_LIMIT = 5


class Database:
    def __init__(self):
        self.db = parameters.DATABASE_INFO["db_name"]
        self.db_user = parameters.DATABASE_INFO["user"]
        self.password = parameters.DATABASE_INFO["password"]
        self.host = parameters.DATABASE_INFO["host"]
        self.port = parameters.DATABASE_INFO["port"]
        self.connection = None
        self.cursor = None


    def connect(self):
        try:
            self.connection = psycopg2.connect(user=self.db_user, password=self.password, host=self.host,
                                               port=self.port,
                                               database=self.db)
            self.cursor = self.connection.cursor()
        except Exception as e:
            assert AssertionError('Can\'t connect to database. Error'.format(e))

    def

class User:
    def __init__(self, name):
        self.name = name
        self.clear_name()


    def clear_name(self):
        """
        Name change protection by spaces
        """
        self.name = ' '.join(name.split())

    def check_db(self):
        sql_query = 'select * from {table} where name = {name}'.format(table = TABLE_NAME, name = self.name)


    def create_new_user(self):
        sql_query = 'insert into {table} values(\'name\', 5'.format(table = TABLE_NAME, name = self.name, access_count = ACCESS_COUNT_LIMIT)

     
    @staticmethod
    def authorization(): 
        pass



if __name__ == "__main__":
    name = input("Print your name: ")
