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
                total float,
                CONSTRAINT unique_date UNIQUE (date)
            )
        '''

        cur.execute(create_script)

        conn.commit()

    except Exception as error:
        print(error)

    def Add_Data(date, cash, credit, other):

        total = cash + credit + other
        try:
            add_script = '''
                INSERT INTO data (date, cash, credit, other, total)
                 VALUES (%s, %s, %s, %s, %s);
            '''
            Postgres.cur.execute(
                add_script, (date, cash, credit, other, total))
            Postgres.conn.commit()
            print("add success")

        except Exception as error:
            print(error)

    def Update_Data(updated_date, update_cash, update_credit, update_other):
        update_total = update_cash + update_credit + update_other
        try:
            update_script = """
                UPDATE data SET cash = %s, credit = %s, other = %s, total = %s
                WHERE date = %s;
            """
            Postgres.cur.execute(
                update_script,
                (update_cash, update_credit, update_other,
                 update_total, updated_date))
            Postgres.conn.commit()

            print("update success")
        except Exception as error:
            print(error)

    def Delete_Data(date):
        delete_script = """
            DELETE FROM data WHERE date = %s;
        """
        Postgres.cur.execute(delete_script, (date,))
        Postgres.conn.commit()
        print("delete sucess")

    def Get_Data(date):
        try:
            select_script = '''
                SELECT * FROM data WHERE date = %s;
            '''
            Postgres.cur.execute(select_script, (date,))
            row = Postgres.cur.fetchone()

            if row:
                print('date:', row[0])
                print('cash:', row[1])
                print('credit:', row[2])
                print('other:', row[3])
                print('total:', row[4])
                print("______________________________________________________")
            else:
                print(f"No data found for date {date}")

            return row

        except Exception as error:
            print(error)

    def Get_All_Data():
        try:
            select_all_script = '''
                SELECT * FROM data;
            '''
            Postgres.cur.execute(select_all_script)
            rows = Postgres.cur.fetchall()

            for row in rows:
                print('date:', row[0])
                print('cash:', row[1])
                print('credit:', row[2])
                print('other:', row[3])
                print('total:', row[4])
                print("______________________________________________________")

            print(rows)
            return rows

        except Exception as error:
            print(error)
