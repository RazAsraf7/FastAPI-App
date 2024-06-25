from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from bson import ObjectId
import uvicorn
import re

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

app = FastAPI()

# Templates for FastAPI
templates = Jinja2Templates(directory="templates")

@app.get('/index/', response_class=HTMLResponse)
async def index(request: Request):
    context = {'request': request}
    return templates.TemplateResponse('index.html', context)

@app.get('/register', response_class=HTMLResponse)
async def register_form(request: Request):
    context = {'request': request}
    return templates.TemplateResponse('register.html', context)

@app.post('/register', response_class=HTMLResponse)
async def register(
    request: Request,
    First_Name: str = Form(...), Last_Name: str = Form(...), User_Name: str = Form(...), Password: str = Form(...),
    Email: str = Form(...), Address: str = Form(...), City: str = Form(...), Gender: str = Form(...), Phone_Number: str = Form(...)
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
        if (existing_username is not None):
            raise HTTPException(status_code=400, detail='Username already exists. Please choose a different username.')

        # Check if user with same email already exists
        existing_email = users_collection.find_one({"email": Email})
        if (existing_email is not None):
            raise HTTPException(status_code=400, detail='Email already exists. Please use a different email address.')

        # Fetch region from Cities collection based on provided City
        result_city = cities_collection.find_one({"name": City})

        if not result_city:
            raise HTTPException(status_code=400, detail=f'Unknown city: {City}. Please provide a valid city.')

        region = result_city['district']

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

        # Redirect to register success page with username as a query parameter
        return RedirectResponse(url=f'/register_success?username={User_Name}', status_code=303)

    except HTTPException as http_err:
        raise http_err
    
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error inserting user into database: {err}")

@app.get('/register_success', response_class=HTMLResponse)
async def register_success(request: Request, username: str):
    context = {'request': request, 'username': username}
    return templates.TemplateResponse('register_success.html', context)

@app.get('/login', response_class=HTMLResponse)
async def login_form(request: Request):
    context = {'request': request}
    return templates.TemplateResponse('login.html', context)

@app.post('/login', response_class=HTMLResponse)
async def login(request: Request, User_Name: str = Form(...), Password: str = Form(...)):
    try:
        # Validate user credentials
        user = users_collection.find_one({"username": User_Name, "password": Password})
        if not user:
            context = {'request': request, 'error': 'Invalid username or password'}
            return templates.TemplateResponse('login.html', context)

        # Redirect to home page after successful login
        return RedirectResponse(url='/index/', status_code=303)
    
    except HTTPException as http_err:
        raise http_err
    
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error during login: {err}")

@app.get('/{user_id}/add_hobby', response_class=HTMLResponse)
async def add_hobby_form(request: Request, user_id: str):
    context = {'request': request, 'user_id': user_id}
    return templates.TemplateResponse('add_hobby.html', context)

@app.post('/{user_id}/add_hobby', response_class=HTMLResponse)
async def add_hobby(user_id: str, hobby: str = Form(...)):
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

        return HTMLResponse(f"Hobby '{hobby}' added successfully for user with user_id: {user_id}")
    
    except HTTPException as http_err:
        raise http_err
    
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error adding hobby: {err}")

@app.get('/ADMIN/show_all_users', response_class=HTMLResponse)
async def show_all_users(request: Request):
    try:
        users = list(users_collection.find({}, {'_id': 0}))  # Do not include _id in the response
        context = {'request': request, 'users': users}
        return templates.TemplateResponse('show_all_users.html', context)
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error retrieving users: {err}")

@app.get('/available_people', response_class=HTMLResponse)
async def get_available_people(request: Request):
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
        context = {'request': request, 'available_people': templist}
        
        return templates.TemplateResponse('available_people.html', context)
    
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error retrieving available people: {err}")

@app.get('/calculator', response_class=HTMLResponse)
async def calculator_form(request: Request):
    context = {'request': request}
    return templates.TemplateResponse('calculator.html', context)

@app.post('/calculator', response_class=HTMLResponse)
async def calculator(request: Request, first_number: int = Form(...), second_number: int = Form(...), action: str = Form(...)) -> int:
    try:
        if action.lower() == 'multiply' or action.lower() == 'multiplication':
            result = first_number * second_number
        elif action.lower() == 'divide' or action.lower() == 'division':
            result = first_number / second_number
        elif action.lower() == 'add' or action.lower() == 'addition':
            result = first_number + second_number
        elif action.lower() == 'subtract' or action.lower() == 'subtraction':
            result = first_number - second_number
        else:
            result = f"Action {action} is not supported. Supported actions are: multiplication, division, addition, subtraction"
        return HTMLResponse(f"Result: {result}")
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error performing calculations: {err}")
    
if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
