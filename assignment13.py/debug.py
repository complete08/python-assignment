import pandas as pd
import mysql.connector


def analyze_db_data():
    conn = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="company_db"
        )

        # Query to fetch all employees
        query = "SELECT * FROM employees"

        # Load the SQL query directly into a DataFrame
        df = pd.read_sql(query, conn)

        # Print the average salary
        print("Average Salary:", df['salary'].mean())

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()


analyze_db_data()