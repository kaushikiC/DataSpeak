
import psycopg2


# Database connection parameters
DB_NAME = "Chinook"
DB_USER = "postgres"
DB_PASSWORD = "@Password1"
DB_HOST = "localhost"
DB_PORT = "5432"

# Connect to PostgreSQL database
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()
    print("Database connection successful")

    

    # Execute a query
    cursor.execute('SELECT * FROM "Album" LIMIT 10;')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    
    # Don't forget to close the cursor and connection
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")