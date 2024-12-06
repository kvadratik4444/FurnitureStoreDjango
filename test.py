import psycopg2

try:
    conn = psycopg2.connect(
        dbname="home",
        user="home",
        password="home",
        host="127.0.0.1",
        port="5432",
    )
    print("Connection successful")
except Exception as e:
    print(f"Error: {e}")
