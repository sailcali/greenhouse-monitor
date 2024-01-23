import psycopg2
from datetime import datetime
import pytz
import os
from dotenv import load_dotenv

load_dotenv()
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")
DB_HOST = os.environ.get("DB_HOST")

conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASS)

def log(temp, hum):
    
    timestamp = datetime.now(tz=pytz.timezone("US/Pacific"))
    cur = conn.cursor()
    cur.execute(f"""INSERT INTO greenhouse (time, temp, humidity) values ('{timestamp}', {temp}, {hum});""")
    conn.commit()
    cur.close()
