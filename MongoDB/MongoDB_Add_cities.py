from pymongo import MongoClient

# MongoDB connection URI
uri = "mongodb+srv://raz:F4vy5JzhUg@dmd.hjdhwf6.mongodb.net/DMD?retryWrites=true&w=majority"

# Cities data in dictionaries
cities = [
    {'name': 'Safed', 'district': 'Northern District'},
    {'name': 'Tiberias', 'district': 'Northern District'},
    {'name': 'Nazareth', 'district': 'Northern District'},
    {'name': 'Nof HaGalil', 'district': 'Northern District'},
    {'name': 'Acre', 'district': 'Northern District'},
    {'name': 'Karmiel', 'district': 'Northern District'},
    {'name': 'Nahariya', 'district': 'Northern District'},
    {'name': 'Migdal HaEmek', 'district': 'Northern District'},
    {'name': 'Ma\'alot-Tarshiha', 'district': 'Northern District'},
    {'name': 'Shfar\'am', 'district': 'Northern District'},
    {'name': 'Sakhnin', 'district': 'Northern District'},
    {'name': 'Kiryat Shmona', 'district': 'Northern District'},
    {'name': 'Yokneam Illit', 'district': 'Northern District'},
    {'name': 'Kiryat Ata', 'district': 'Northern District'},
    {'name': 'Kiryat Bialik', 'district': 'Northern District'},
    {'name': 'Kiryat Yam', 'district': 'Northern District'},
    {'name': 'Tamra', 'district': 'Northern District'},
    {'name': 'Haifa', 'district': 'Haifa District'},
    {'name': 'Hadera', 'district': 'Haifa District'},
    {'name': 'Or Akiva', 'district': 'Haifa District'},
    {'name': 'Nesher', 'district': 'Haifa District'},
    {'name': 'Tirat Carmel', 'district': 'Haifa District'},
    {'name': 'Baqa al-Gharbiyye', 'district': 'Haifa District'},
    {'name': 'Umm al-Fahm', 'district': 'Haifa District'},
    {'name': 'Zikhron Ya\'akov', 'district': 'Haifa District'},
    {'name': 'Pardes Hanna-Karkur', 'district': 'Haifa District'},
    {'name': 'Petah Tikva', 'district': 'Central District'},
    {'name': 'Netanya', 'district': 'Central District'},
    {'name': 'Raanana', 'district': 'Central District'},
    {'name': 'Herzliya', 'district': 'Central District'},
    {'name': 'Kfar Saba', 'district': 'Central District'},
    {'name': 'Hod HaSharon', 'district': 'Central District'},
    {'name': 'Rosh HaAyin', 'district': 'Central District'},
    {'name': 'Tira', 'district': 'Central District'},
    {'name': 'Ramat HaSharon', 'district': 'Central District'},
    {'name': 'Bat Yam', 'district': 'Central District'},
    {'name': 'Holon', 'district': 'Central District'},
    {'name': 'Rishon LeZion', 'district': 'Central District'},
    {'name': 'Givatayim', 'district': 'Central District'},
    {'name': 'Or Yehuda', 'district': 'Central District'},
    {'name': 'Yavne', 'district': 'Central District'},
    {'name': 'Lod', 'district': 'Central District'},
    {'name': 'Ramla', 'district': 'Central District'},
    {'name': 'Modiin-Maccabim-Reut', 'district': 'Central District'},
    {'name': 'Kiryat Ono', 'district': 'Central District'},
    {'name': 'Yehud-Monosson', 'district': 'Central District'},
    {'name': 'Tel Aviv-Yafo', 'district': 'Tel Aviv District'},
    {'name': 'Bnei Brak', 'district': 'Tel Aviv District'},
    {'name': 'Ramat Gan', 'district': 'Tel Aviv District'},
    {'name': 'Givatayim', 'district': 'Tel Aviv District'},
    {'name': 'Bat Yam', 'district': 'Tel Aviv District'},
    {'name': 'Holon', 'district': 'Tel Aviv District'},
    {'name': 'Jerusalem', 'district': 'Jerusalem District'},
    {'name': 'Beit Shemesh', 'district': 'Jerusalem District'},
    {'name': 'Ma\'ale Adumim', 'district': 'Jerusalem District'},
    {'name': 'Modi\'in Illit', 'district': 'Jerusalem District'},
    {'name': 'Beersheba', 'district': 'Southern District'},
    {'name': 'Ashdod', 'district': 'Southern District'},
    {'name': 'Ashkelon', 'district': 'Southern District'},
    {'name': 'Eilat', 'district': 'Southern District'},
    {'name': 'Dimona', 'district': 'Southern District'},
    {'name': 'Kiryat Gat', 'district': 'Southern District'},
    {'name': 'Netivot', 'district': 'Southern District'},
    {'name': 'Ofakim', 'district': 'Southern District'},
    {'name': 'Sderot', 'district': 'Southern District'},
    {'name': 'Arad', 'district': 'Southern District'},
    {'name': 'Rahat', 'district': 'Southern District'},
    {'name': 'Modi\'in Illit', 'district': 'Judea and Samaria Area'},
    {'name': 'Ariel', 'district': 'Judea and Samaria Area'},
    {'name': 'Ma\'ale Adumim', 'district': 'Judea and Samaria Area'},
    {'name': 'Beitar Illit', 'district': 'Judea and Samaria Area'},
    {'name': 'Kiryat Arba', 'district': 'Judea and Samaria Area'},
    {'name': 'Giv\'at Ze\'ev', 'district': 'Judea and Samaria Area'},
    {'name': 'Rosh HaNikra', 'district': 'Northern District'},
    {'name': 'Jezreel Valley', 'district': 'Northern District'},
    {'name': 'Herzliya Pituach', 'district': 'Central District'},
    {'name': 'Azor', 'district': 'Central District'},
    {'name': 'Mevasseret Zion', 'district': 'Jerusalem District'},
    {'name': 'Tzur Hadassah', 'district': 'Jerusalem District'},
    {'name': 'Shoham', 'district': 'Central District'},
    {'name': 'Kfar Shmaryahu', 'district': 'Central District'},
    {'name': 'Migdal', 'district': 'Northern District'},
    {'name': 'Kfar Yona', 'district': 'Central District'},
    {'name': 'Kiryat Tiv\'on', 'district': 'Northern District'},
    {'name': 'Bnei Ayish', 'district': 'Central District'},
    {'name': 'Tirat Yehuda', 'district': 'Central District'},
    {'name': 'Mitzpe Ramon', 'district': 'Southern District'}
]

# Connect to MongoDB
client = MongoClient(uri)

# Access database and collection
db = client['DMD']
collection = db['cities']

# Insert the data into MongoDB
result = collection.insert_many(cities)

# Output the result
print(f"Inserted {len(result.inserted_ids)} documents")

# Close the MongoDB connection
client.close()
