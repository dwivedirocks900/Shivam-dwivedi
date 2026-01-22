import os
import mysql.connector
from mysql.connector import Error


def get_mysql_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",                 # ✅ fixed
            user="root",
            password=os.getenv("MYSQL_PASSWORD"),
            database="test_db"
        )

        if connection.is_connected():
            print("✅ MySQL connection successful")
            return connection

    except Error as err:
        print("❌ MYSQL ERROR:", err)
        return None


def close_connection(connection):
    if connection and connection.is_connected():
        connection.close()
        print("🔒 Connection closed")


# -------- Main Execution --------
conn = get_mysql_connection()

if conn:
    cursor = None
    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT customer_id, customer_name, amount
            FROM Customer_details
            ORDER BY amount DESC
            LIMIT 2
        """)

        results = cursor.fetchall()
        for row in results:
            print(row)

        print("✅ Table has been sorted successfully")

    except Error as e:
        print("❌ Error while executing SQL:", e)

    finally:
        if cursor:
            cursor.close()
        close_connection(conn)
