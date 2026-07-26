import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()  # reads variables from .env into the environment

connection = psycopg2.connect(os.getenv("DATABASE_URL"))

cursor = connection.cursor()
cursor.execute("SELECT version();")
result = cursor.fetchone()

print("✅ Connected successfully!")
print("PostgreSQL version:", result[0])

cursor.close()
connection.close()