import psycopg2
import os
from dotenv import load_dotenv


class Postgres:
    load_dotenv()
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(
            host=os.environ.get("hostname"),
            database=os.environ.get('database'),
            user=os.environ.get('username'),
            password=os.environ.get('password'),
            port=os.environ.get('port_id')
        )
        cur = conn.cursor()

        create_script = '''
            CREATE TABLE IF NOT EXISTS data(
                date  varchar(30) not Null,
                cash  float,
                credit  float,
                other  float,
                total float
            )
        '''

        cur.execute(create_script)

        conn.commit()

    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

    date = '5/5/2023'
    cash = 23.0
    credit = 35.0
    other = 45.0
    total = cash + credit + other

    def Add(date, cash, credit, other, total, self):
        date = self.date
        cash = self.cash
        credit = self.credit
        other = self.other
        total = self.total

        try:
            add_script = '''
                INSERT INTO data (date, cash, credit, other, total) VALUES ((?),(?), (?), (?), (?)) 
            '''
            self.cur.execute(add_script, (date, cash, credit, other, total))
            self.conn.commit()

            self.conn.close()

        except Exception as error:
            print(error)

    def Update():
        update_script = """
            UPDATE data SET 
        """

    def Delete():
        delete_script = """
            DELETE FROM data
        """

    def Get():
        get_script = """
            SELECT * FROM data
        """

    def GetAll():
        get_all_script = """
            SELECT * FROM data
        """
