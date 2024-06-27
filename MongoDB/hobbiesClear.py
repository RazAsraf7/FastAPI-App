from pymongo import MongoClient
# MongoDB connection URI
uri = "mongodb+srv://raz:F4vy5JzhUg@dmd.hjdhwf6.mongodb.net/DMD?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)

# Access database and collections
db = client['DMD']
users_collection = db['users']
hobbies_collection = db['hobbies']
cities_collection = db['cities']

# Check MongoDB connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

try:
    hobbies_collection.delete_many({})
    print("Hobbies deleted successfully.")
except Exception as e:
    print(f"Error deleting users: {e}")

# Close the MongoDB connection
client.close()