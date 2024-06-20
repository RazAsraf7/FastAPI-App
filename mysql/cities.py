import mysql.connector

# Database connection
connection = mysql.connector.connect(
    host='localhost',
    port=3307,
    user='raz',
    password='123456',
    database='DMD_users'
)

cursor = connection.cursor()

# Create table
create_table_query = """
CREATE TABLE IF NOT EXISTS Cities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    region VARCHAR(255) NOT NULL
)
"""
cursor.execute(create_table_query)

# Data to be inserted
cities = {
    "Northern District": [
        "Safed", "Tiberias", "Nazareth", "Nof HaGalil", "Acre", "Karmiel",
        "Nahariya", "Migdal HaEmek", "Ma'alot-Tarshiha", "Shfar'am", "Sakhnin",
        "Kiryat Shmona", "Yokneam Illit", "Kiryat Ata", "Kiryat Bialik", "Kiryat Yam", "Tamra"
    ],
    "Haifa District": [
        "Haifa", "Hadera", "Or Akiva", "Nesher", "Tirat Carmel", "Baqa al-Gharbiyye",
        "Umm al-Fahm", "Zikhron Ya'akov", "Pardes Hanna-Karkur"
    ],
    "Central District": [
        "Petah Tikva", "Netanya", "Raanana", "Herzliya", "Kfar Saba", "Hod HaSharon",
        "Rosh HaAyin", "Tira", "Ramat HaSharon", "Bat Yam", "Holon", "Rishon LeZion",
        "Givatayim", "Or Yehuda", "Yavne", "Lod", "Ramla", "Modiin-Maccabim-Reut",
        "Kiryat Ono", "Yehud-Monosson"
    ],
    "Tel Aviv District": [
        "Tel Aviv-Yafo", "Bnei Brak", "Ramat Gan", "Givatayim", "Bat Yam", "Holon"
    ],
    "Jerusalem District": [
        "Jerusalem", "Beit Shemesh", "Ma'ale Adumim", "Modi'in Illit"
    ],
    "Southern District": [
        "Beersheba", "Ashdod", "Ashkelon", "Eilat", "Dimona", "Kiryat Gat",
        "Netivot", "Ofakim", "Sderot", "Arad", "Rahat"
    ],
    "Judea and Samaria Area": [
        "Modi'in Illit", "Ariel", "Ma'ale Adumim", "Beitar Illit", "Kiryat Arba", "Giv'at Ze'ev"
    ]
}

# Insert data into the table
insert_city_query = "INSERT INTO Cities (name, region) VALUES (%s, %s)"
for region, cities_list in cities.items():
    for city in cities_list:
        cursor.execute(insert_city_query, (city, region))

# Commit changes and close connection
connection.commit()
cursor.close()
connection.close()
