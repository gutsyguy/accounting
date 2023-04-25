import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

mydb = mysql.connector.connect(
    host = "localhost",
    user = "user",
    password = os.environ.get("MYSQL_PASSWORD"),
    database = "database"
)

cursor = mydb.cursor()

cursor.execute("CREATE DATABASE info")