from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
USERNAME = os.getenv("USERNAME")
ROOT_PASSWORD = os.getenv("ROOT_PASSWORD")
PORT = os.getenv("PORT")
HOST = os.getenv("HOST")
# MongoDB connection URI
uri = f"mongodb://{USERNAME}:{ROOT_PASSWORD}@{HOST}:{PORT}/"

# Cities data in dictionaries
cities = [
    {'name': 'Acre', 'district': 'Northern District'},
    {'name': 'Arad', 'district': 'Southern District'},
    {'name': 'Ariel', 'district': 'Judea and Samaria Area'},
    {'name': 'Ashdod', 'district': 'Southern District'},
    {'name': 'Ashkelon', 'district': 'Southern District'},
    {'name': 'Azor', 'district': 'Central District'},
    {'name': 'Baqa al-Gharbiyye', 'district': 'Haifa District'},
    {'name': 'Bat Yam', 'district': 'Tel Aviv District'},
    {'name': 'Beersheba', 'district': 'Southern District'},
    {'name': 'Beit Shemesh', 'district': 'Jerusalem District'},
    {'name': 'Beitar Illit', 'district': 'Judea and Samaria Area'},
    {'name': 'Bnei Ayish', 'district': 'Central District'},
    {'name': 'Bnei Brak', 'district': 'Tel Aviv District'},
    {'name': 'Dimona', 'district': 'Southern District'},
    {'name': 'Eilat', 'district': 'Southern District'},
    {'name': 'Giv\'at Ze\'ev', 'district': 'Judea and Samaria Area'},
    {'name': 'Givatayim', 'district': 'Tel Aviv District'},
    {'name': 'Hadera', 'district': 'Haifa District'},
    {'name': 'Haifa', 'district': 'Haifa District'},
    {'name': 'Herzliya', 'district': 'Central District'},
    {'name': 'Herzliya Pituach', 'district': 'Central District'},
    {'name': 'Hod HaSharon', 'district': 'Central District'},
    {'name': 'Holon', 'district': 'Tel Aviv District'},
    {'name': 'Jerusalem', 'district': 'Jerusalem District'},
    {'name': 'Jezreel Valley', 'district': 'Northern District'},
    {'name': 'Karmiel', 'district': 'Northern District'},
    {'name': 'Kfar Saba', 'district': 'Central District'},
    {'name': 'Kfar Shmaryahu', 'district': 'Central District'},
    {'name': 'Kfar Yona', 'district': 'Central District'},
    {'name': 'Kiryat Arba', 'district': 'Judea and Samaria Area'},
    {'name': 'Kiryat Ata', 'district': 'Northern District'},
    {'name': 'Kiryat Bialik', 'district': 'Northern District'},
    {'name': 'Kiryat Gat', 'district': 'Southern District'},
    {'name': 'Kiryat Ono', 'district': 'Central District'},
    {'name': 'Kiryat Shmona', 'district': 'Northern District'},
    {'name': 'Kiryat Tiv\'on', 'district': 'Northern District'},
    {'name': 'Kiryat Yam', 'district': 'Northern District'},
    {'name': 'Lod', 'district': 'Central District'},
    {'name': 'Ma\'ale Adumim', 'district': 'Judea and Samaria Area'},
    {'name': 'Ma\'alot-Tarshiha', 'district': 'Northern District'},
    {'name': 'Mevasseret Zion', 'district': 'Jerusalem District'},
    {'name': 'Migdal', 'district': 'Northern District'},
    {'name': 'Migdal HaEmek', 'district': 'Northern District'},
    {'name': 'Modi\'in Illit', 'district': 'Judea and Samaria Area'},
    {'name': 'Modiin-Maccabim-Reut', 'district': 'Central District'},
    {'name': 'Nahariya', 'district': 'Northern District'},
    {'name': 'Nazareth', 'district': 'Northern District'},
    {'name': 'Nesher', 'district': 'Haifa District'},
    {'name': 'Netanya', 'district': 'Central District'},
    {'name': 'Netivot', 'district': 'Southern District'},
    {'name': 'Nof HaGalil', 'district': 'Northern District'},
    {'name': 'Ofakim', 'district': 'Southern District'},
    {'name': 'Or Akiva', 'district': 'Haifa District'},
    {'name': 'Or Yehuda', 'district': 'Central District'},
    {'name': 'Pardes Hanna-Karkur', 'district': 'Haifa District'},
    {'name': 'Petah Tikva', 'district': 'Central District'},
    {'name': 'Raanana', 'district': 'Central District'},
    {'name': 'Ramat Gan', 'district': 'Tel Aviv District'},
    {'name': 'Ramat HaSharon', 'district': 'Central District'},
    {'name': 'Ramla', 'district': 'Central District'},
    {'name': 'Rishon LeZion', 'district': 'Central District'},
    {'name': 'Rosh HaAyin', 'district': 'Central District'},
    {'name': 'Rosh HaNikra', 'district': 'Northern District'},
    {'name': 'Safed', 'district': 'Northern District'},
    {'name': 'Sakhnin', 'district': 'Northern District'},
    {'name': 'Sderot', 'district': 'Southern District'},
    {'name': 'Shfar\'am', 'district': 'Northern District'},
    {'name': 'Shoham', 'district': 'Central District'},
    {'name': 'Tamra', 'district': 'Northern District'},
    {'name': 'Tel Aviv-Yafo', 'district': 'Tel Aviv District'},
    {'name': 'Tiberias', 'district': 'Northern District'},
    {'name': 'Tirat Carmel', 'district': 'Haifa District'},
    {'name': 'Tirat Yehuda', 'district': 'Central District'},
    {'name': 'Tira', 'district': 'Central District'},
    {'name': 'Tzur Hadassah', 'district': 'Jerusalem District'},
    {'name': 'Umm al-Fahm', 'district': 'Haifa District'},
    {'name': 'Yavne', 'district': 'Central District'},
    {'name': 'Yehud-Monosson', 'district': 'Central District'},
    {'name': 'Yokneam Illit', 'district': 'Northern District'},
    {'name': 'Zikhron Ya\'akov', 'district': 'Haifa District'}
]

# Connect to MongoDB
client = MongoClient(uri)

# Access database and collection
db = client['DMD']
collection = db['cities']

# Insert the data into MongoDB only if not present
for city in cities:
    if not collection.find_one({'name': city['name']}):
        collection.insert_one(city)

# Output the result
print(f"Inserted {len(cities)} documents if not already present")

# Close the MongoDB connection
client.close()
