import psycopg2
from conf import database, user, password, host, port


class MyDatabase:
    def __init__(self):
        self.conn = psycopg2.connect(dbname=database,
                                     user=user,
                                     password=password,
                                     host=host,
                                     port=port
                                     )
        self.cur = self.conn.cursor()

    def select(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()

    def insert(self, query):
        self.cur.execute(query)
        self.conn.commit()

    def delete(self, query):
        self.insert(query)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()
        self.conn.close()
