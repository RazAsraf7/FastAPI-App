import mysql.connector

# Establish a connection to the MySQL database
connection = mysql.connector.connect(
    host="127.0.0.1",
    port='3307',
    user="raz",
    password="123456",
    database="DMD_users"
)

cursor = connection.cursor()

# List of cities to be inserted
cities = [
    ('Rosh HaNikra', 'Northern District'),
    ('Jezreel Valley', 'Northern District'),
    ('Herzliya Pituach', 'Central District'),
    ('Azor', 'Central District'),
    ('Mevasseret Zion', 'Jerusalem District'),
    ('Tzur Hadassah', 'Jerusalem District'),
    ('Shoham', 'Central District'),
    ('Kfar Shmaryahu', 'Central District'),
    ('Migdal', 'Northern District'),
    ('Kfar Yona', 'Central District'),
    ('Kiryat Tiv\'on', 'Northern District'),
    ('Bnei Ayish', 'Central District'),
    ('Tirat Yehuda', 'Central District'),
    ('Mitzpe Ramon', 'Southern District')
]

# SQL query to insert a city
sql_query = "INSERT INTO Cities (name, region) VALUES (%s, %s)"

# Insert each city into the database
for city in cities:
    cursor.execute(sql_query, city)

# Commit the changes
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()

print("Cities inserted successfully.")
