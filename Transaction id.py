import os
import mysql.connector
from mysql.connector import Error


def get_mysql_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
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

        # ✅ UPDATE existing rows (correct approach)
        cursor.execute("""
            UPDATE Customer_details
            SET Transaction_id = CASE CUSTOMER_NAME
                WHEN 'Shivam' THEN 1997
                WHEN 'Amit'   THEN 2000
                WHEN 'Neha'   THEN 1998
                WHEN 'Ravi'   THEN 1995
            END
            WHERE CUSTOMER_NAME IS NOT NULL
        """)
        cursor.execute("""DELETE FROM Customer_details
        WHERE CUSTOMER_NAME IS NULL
        AND CUSTOMER_id IS NULL;""")


        conn.commit()
        print("✅ Transaction_id updated successfully")

    except Error as e:
        print("❌ Error while executing SQL:", e)

    finally:
        if cursor:
            cursor.close()
        close_connection(conn)
