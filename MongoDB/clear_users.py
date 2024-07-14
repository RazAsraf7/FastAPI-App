from pymongo import MongoClient

# MongoDB connection URI
uri = "mongodb+srv://raz:F4vy5JzhUg@dmd.hjdhwf6.mongodb.net/DMD?retryWrites=true&w=majority"

# Connect to MongoDB
client = MongoClient(uri)

# Access database and collection
db = client['DMD']
collection = db['users']

# Check if the collection exists and then delete documents
if 'users' in db.list_collection_names():
    result = collection.delete_many({})
    print(f"Deleted {result.deleted_count} documents from the 'users' collection")
else:
    print("The 'users' collection does not exist")

db.create_collection('users')

# Close the MongoDB connection
client.close()
