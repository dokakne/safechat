import psycopg2

# Connect to your postgres DB
conn = psycopg2.connect("user=REDACTED password=REDACTED")

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a query
cur.execute("SELECT * FROM test")

# Retrieve query results
records = cur.fetchall()
print(records)
