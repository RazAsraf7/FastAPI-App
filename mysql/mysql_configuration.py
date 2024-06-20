import mysql.connector
import json

# def create_table(cursor):
    # Create table if not exists
    # cursor.execute("""
        # CREATE TABLE IF NOT EXISTS CityDistricts (
    #         id INT AUTO_INCREMENT PRIMARY KEY,
    #         city_name VARCHAR(100) NOT NULL,
    #         district_name VARCHAR(100) NOT NULL,
    #         UNIQUE KEY unique_city_district (city_name, district_name)
    #     )
    # """)

# def insert_data(cursor):
    # List of cities and their districts
    # cities_districts = [
    #     ('Jerusalem', 'Jerusalem District'),
    #     ('Tel Aviv', 'Tel Aviv District'),
    #     ('Haifa', 'Haifa District'),
    #     ('Rishon LeZion', 'Central District'),
    #     ('Petah Tikva', 'Central District'),
    #     ('Ashdod', 'Southern District'),
    #     ('Netanya', 'Central District'),
    #     ('Beer Sheva', 'Southern District'),
    #     ('Holon', 'Tel Aviv District'),
    #     ('Bnei Brak', 'Tel Aviv District'),
    #     ('Rehovot', 'Central District'),
    #     ('Bat Yam', 'Tel Aviv District'),
    #     ('Kfar Saba', 'Central District'),
    #     ('Modiin-Maccabim-Reut', 'Central District'),
    #     ('Herzliya', 'Tel Aviv District'),
    #     ('Ramat Gan', 'Tel Aviv District'),
    #     ('Ashkelon', 'Southern District'),
    #     ('Lod', 'Central District'),
    #     ('Ramat HaSharon', 'Tel Aviv District'),
    #     ('Ra''anana', 'Central District'),
    #     ('Be''er Ya''akov', 'Central District'),
    #     ('Hod HaSharon', 'Central District'),
    #     ('Kiryat Ata', 'Haifa District'),
    #     ('Giv''atayim', 'Tel Aviv District'),
    #     ('Ra''at', 'Northern District'),
    #     ('Karmiel', 'Northern District'),
    #     ('Yavne', 'Central District'),
    #     ('Or Yehuda', 'Tel Aviv District'),
    #     ('Kiryat Bialik', 'Haifa District'),
    #     ('Kiryat Motzkin', 'Haifa District'),
    #     ('Giv''at Shmuel', 'Central District'),
    #     ('Rosh HaAyin', 'Central District'),
    #     ('Nesher', 'Haifa District'),
    #     ('Dimona', 'Southern District'),
    #     ('Sderot', 'Southern District'),
    #     ('Tamra', 'Northern District'),
    #     ('Kiryat Yam', 'Haifa District'),
    #     ('Kiryat Gat', 'Southern District'),
    #     ('Afula', 'Northern District'),
    #     ('Nof Hagalil', 'Northern District'),
    #     ('Qalansawe', 'Central District'),
    #     ('Umm al-Fahm', 'Northern District'),
    #     ('Eilat', 'Southern District'),
    #     ('Beit She''an', 'Northern District'),
    #     ('Nazareth Illit', 'Northern District'),
    #     ('Kiryat Malakhi', 'Southern District'),
    #     ('Tira', 'Central District'),
    #     ('Hod HaSharon', 'Central District'),
    #     ('Sakhnin', 'Northern District'),
    #     ('Kiryat Shmona', 'Northern District'),
    #     ('Yehud-Monosson', 'Central District'),
    #     ('Sderot', 'Southern District'),
    #     ('Netivot', 'Southern District'),
    #     ('Tiberias', 'Northern District'),
    #     ('Ofakim', 'Southern District'),
    #     ('Yeruham', 'Southern District'),
    #     ('Modi''in Illit', 'Central District'),
    #     ('Yavne', 'Central District'),
    #     ('Tzfat', 'Northern District'),
    #     ('Mevaseret Zion', 'Jerusalem District'),
    #     ('Dimona', 'Southern District'),
    #     ('Kiryat Gat', 'Southern District')
    # ]

    # Insert data into the table
# for city, district in cities_districts:
#     cursor.execute("""
#             INSERT INTO CityDistricts (city_name, district_name)
#             VALUES (%s, %s)
#             ON DUPLICATE KEY UPDATE
#             city_name = VALUES(city_name),
#             district_name = VALUES(district_name)
#         """, (city, district))

# def main():
#     # Connect to the MySQL server
#     conn = mysql.connector.connect(
#         host='localhost',  # Change this to your MySQL server host
#         port=3307,
#         user='raz',  # Change this to your MySQL username
#         password='123456',  # Change this to your MySQL password
#         database='DMD_users'
#     )

#     # Create cursor
#     cursor = conn.cursor()

#     # Create table
#     # create_table(cursor)

#     # Insert data
#     # insert_data(cursor)

#     # Commit changes and close cursor and connection
#     conn.commit()
#     cursor.close()
#     conn.close()

# if __name__ == "__main__":
#     main()


# Database connection configuration
config = {
    'user': 'raz',
    'password': '123456',
    'host': 'localhost',
    'port': '3307',
    'database': 'DMD_users',
}

# Connect to the database
conn = mysql.connector.connect(**config)
cursor = conn.cursor(dictionary=True)

# Query to select user details
query = "SELECT * FROM users"

cursor.execute(query)

# Fetch all rows from the executed query
rows = cursor.fetchall()

# Write rows to a JSON file
with open('user_details.json', 'w') as json_file:
    json.dump(rows, json_file, indent=4)

# Close cursor and connection
cursor.close()
conn.close()