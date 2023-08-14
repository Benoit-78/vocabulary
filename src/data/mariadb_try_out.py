import mysql.connector


# Connection parameters
config = {
    "user": "root",
    "password": "IBM-vocabulary7",
    "database": "vocabulary",
    "host": "127.0.0.1",
    "port": "3306"
}


try:
    # Create a connection
    conn = mysql.connector.connect(**config)
    # Perform your database operations here
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM version_voc")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    # Close the cursor and connection
    cursor.close()
    conn.close()
except mysql.connector.Error as e:
    print("Error:", e)
