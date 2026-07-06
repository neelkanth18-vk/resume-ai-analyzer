import pymysql

print("Connecting to MySQL to create the database...")
try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root123'
    )
    with connection.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS resume_ai_db;")
    connection.commit()
    print("Success: Database 'resume_ai_db' created successfully!")
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'connection' in locals() and connection.open:
        connection.close()
