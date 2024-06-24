from fastapi import FastAPI, HTTPException, Response
import re
import uvicorn
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId

uri = "mongodb+srv://raz:F4vy5JzhUg@dmd.hjdhwf6.mongodb.net/?retryWrites=true&w=majority&appName=DMD"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Select the database and collections
db = client['dmd']
users_collection = db['users']
cities_collection = db['cities']
hobbies_collection = db['hobbies']

app = FastAPI()

# Register a new user
@app.post('/register')
async def register(
    First_Name: str, Last_Name: str, User_Name: str, Password: str,
    Email: str, Address: str, City: str, Gender: str, Phone_Number: str
):
    try:
        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", Email):
            raise HTTPException(status_code=400, detail='Email is not valid. Please try again')
        
        # Validate password format (only letters and numbers)
        if not Password.isalnum():
            raise HTTPException(status_code=400, detail='Only letters and numbers are supported in password (A-Z, a-z, 0-9)')
        
        # Validate username format (letters, numbers, underscores; cannot start with a number)
        if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", User_Name):
            raise HTTPException(status_code=400, detail='Username must only contain letters, numbers, or underscores, and cannot start with a number.')

        # Check if user with same username already exists
        existing_username = users_collection.find_one({"username": User_Name})
        if existing_username:
            raise HTTPException(status_code=400, detail='Username already exists. Please choose a different username.')

        # Check if user with same email already exists
        existing_email = users_collection.find_one({"email": Email})
        if existing_email:
            raise HTTPException(status_code=400, detail='Email already exists. Please use a different email address.')

        # Fetch region from Cities collection based on provided City
        result_city = cities_collection.find_one({"name": City})

        if not result_city:
            raise HTTPException(status_code=400, detail=f'Unknown city: {City}. Please provide a valid city.')

        region = result_city['region']

        # Prepare user data for insertion
        user_data = {
            "firstname": First_Name,
            "lastname": Last_Name,
            "gender": Gender,
            "phone_number": Phone_Number,
            "full_address": f'{Address}, {City}',
            "city": City,
            "region": region,
            "username": User_Name,
            "email": Email,
            "password": Password,
            "full_name": f'{First_Name} {Last_Name}'
        }

        # Insert the new user into the users collection
        users_collection.insert_one(user_data)

        return f'Successfully created user {User_Name}'
    
    except HTTPException as http_err:
        raise http_err
    
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error inserting user into database: {err}")

# Add hobby for a user
@app.post('/add_hobby')
async def add_hobby(user_id: str, hobby: str):
    try:
        # Convert user_id to ObjectId
        user_id = ObjectId(user_id)

        # Check if the user_id exists in the users collection
        existing_user = users_collection.find_one({"_id": user_id})
        if not existing_user:
            raise HTTPException(status_code=404, detail=f"User with user_id {user_id} not found.")

        # Insert the hobby for the user into the hobbies collection
        hobby_data = {
            "user_id": user_id,
            "hobby": hobby
        }
        
        hobbies_collection.insert_one(hobby_data)

        return {"message": f"Hobby '{hobby}' added successfully for user with user_id: {user_id}"}
    
    except HTTPException as http_err:
        raise http_err
    
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error adding hobby: {err}")

# Get all users endpoint
@app.get('/ADMIN/show_all_users')
async def show_all_users():
    try:
        users = list(users_collection.find({}, {'_id': 0}))  # Do not include _id in the response
        return {"users": users}
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error retrieving users: {err}")

# Get available people with hobbies endpoint
@app.get('/available_people')
async def get_available_people():
    try:
        available_people = list(users_collection.aggregate([
            {
                '$lookup': {
                    'from': 'hobbies',
                    'localField': '_id',
                    'foreignField': 'user_id',
                    'as': 'hobbies'
                }
            },
            {
                '$unwind': '$hobbies'
            },
            {
                '$project': {
                    'firstname': 1,
                    'hobby': '$hobbies.hobby'
                }
            }
        ]))
        
        templist = [f"{person['firstname']} enjoys {person['hobby']}" for person in available_people]
        
        return {'available_people': templist}
    
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error retrieving available people: {err}")

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=5500)
