import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()  # reads variables from .env into the environment

connection = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)

cursor = connection.cursor()
cursor.execute("SELECT version();")
result = cursor.fetchone()

print("✅ Connected successfully!")
print("PostgreSQL version:", result[0])

cursor.close()
connection.close()