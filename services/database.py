import psycopg2
from psycopg2.extras import DictCursor


class Database:
    def __init__(self, connection_options):
        self.dsn = connection_options["dsn"]
        self.conn = psycopg2.connect(self.dsn, cursor_factory=DictCursor)
        self.cursor = self.conn.cursor()

    def execute_query(self, query: str, params=()):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except Exception as ex:
            self.rollback()
            raise ex

    def get_one(self, query: str, params=()):
        try:
            self.cursor.execute(query, params)
            result = self.cursor.fetchone()
            return dict(result) if result else None
        except Exception as ex:
            self.rollback()
            raise ex

    def get_all(self, query: str, params=()):
        try:
            self.cursor.execute(query, params)
            result = self.cursor.fetchall()
            return [dict(row) for row in result]
        except Exception as ex:
            self.rollback()
            raise ex

    def execute_script(self, sql_data: str):
        self.cursor.execute(sql_data)
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()
