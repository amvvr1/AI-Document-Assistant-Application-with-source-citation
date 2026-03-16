from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

try:
    connection = psycopg2.connect(DATABASE_URL)
    print("Connection successful!")
    connection.close()
except Exception as e:
    print(f"Connection failed: {e}")