import mysql.connector

# Establish a connection
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='family_office'
)


cursor = connection.cursor()

if connection.is_connected():
    print("Connected to the database!")

# Execute a query
cursor.execute('SELECT * FROM users')

# Fetch all rows
rows = cursor.fetchall()

# Process the fetched data
for row in rows:
   print(row)


cursor.close()
connection.close()