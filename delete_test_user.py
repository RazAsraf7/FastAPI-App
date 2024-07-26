from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
username = os.getenv("ROOT_USERNAME")
password = os.getenv("ROOT_PASSWORD")
port = os.getenv("PORT")
host = os.getenv("HOST")

# MongoDB connection details
mongo_host = "localhost"
mongo_port = 27017
mongo_db = "DMD"
collection_name = "users"
username_to_delete = "testuser"

client = MongoClient(f"mongodb://{username}:{password}@{mongo_host}:{mongo_port}/")
db = client[mongo_db]
collection = db[collection_name]

try:
# Delete the user
    result = collection.delete_one({"User_Name": username_to_delete})
    print(f"Deleted {result.deleted_count} document(s)")

except Exception as e:
    print(f"Error deleting user: {e}")