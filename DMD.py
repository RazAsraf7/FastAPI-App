from fastapi import FastAPI, HTTPException, Request, Form, Cookie, Response  # Import Response here
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from fastapi.logger import logger
from pymongo import MongoClient, ReturnDocument
from bson import ObjectId
import json
import uvicorn
import re

# MongoDB connection URI
uri = "mongodb://localhost:27017/"

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

# Dummy authentication cookie (replace with your actual authentication method)
def is_authenticated(request: Request) -> bool:
    return "username" in request.cookies

@app.get('/', response_class=HTMLResponse)
async def index(request: Request, username: str = Cookie(default=None)):
    context = {'request': request, 'user_name': username}
    return templates.TemplateResponse('index.html', context)

@app.get('/register', response_class=HTMLResponse)
async def register_form(request: Request):
    try:
        # Fetch cities from MongoDB
        cities = list(cities_collection.find({}, {"_id": 0, "name": 1}))
        context = {'request': request, 'cities': cities}
        return templates.TemplateResponse('register.html', context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching cities: {e}")

@app.post('/register')
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
        hobbies_collection.insert_one({"username":User_Name})

        # Redirect to the success page with user details in query parameters
        return RedirectResponse(url=f'/register_success?User_Name={User_Name}&Full_Name={First_Name} {Last_Name}&Email={Email}&City={City}&Gender={Gender}', status_code=302)

    except HTTPException as http_err:
        raise http_err
    
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error inserting user into database: {err}")

@app.get('/register_success', response_class=HTMLResponse)
async def register_success(request: Request, User_Name: str, Full_Name: str, Email: str, City: str, Gender: str):
    context = {
        'request': request,
        'User_Name': User_Name,
        'Full_Name': Full_Name,
        'Email': Email,
        'City': City,
        'Gender': Gender
    }
    return templates.TemplateResponse('register_success.html', context)


@app.get('/login', response_class=HTMLResponse)
async def login_form(request: Request):
    context = {'request': request}
    return templates.TemplateResponse('login.html', context)

@app.post('/login', response_class=HTMLResponse)
async def login(request: Request, User_Name: str = Form(...), Password: str = Form(...)):
    if User_Name == 'admin' and Password == 'adminPassword':
        return RedirectResponse(url='/ADMIN', status_code=303)
    try:
        # Validate user credentials
        user = users_collection.find_one({"username": User_Name, "password": Password})
        if not user:
            context = {'request': request, 'error': 'Invalid username or password'}
            return templates.TemplateResponse('login.html', context)

        # Set username in cookie (dummy authentication, replace with your actual authentication method)
        response = RedirectResponse(url=f'/profile/{User_Name}', status_code=303)
        response.set_cookie(key="username", value=User_Name)
        return response
    
    except HTTPException as http_err:
        raise http_err
    
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error during login: {err}")

@app.get('/logout', response_class=HTMLResponse)
async def logout(request: Request):
    response = RedirectResponse(url='/login', status_code=303)
    response.delete_cookie("user_name")
    return response

def retrieve_user_id(user_name):
    user = users_collection.find_one({"username": user_name})
    if user:
        return user['_id']
    else:
        return None

def retrieve_username(user_id):
    user = users_collection.find_one({"_id": user_id})
    if user:
        return user['username']
    else:
        return None
    
@app.get('/api/hobbies/{username}', response_class=HTMLResponse)
def get_user_hobbies(username):
    pipeline = [
        {"$match": {"username": username}},
        {"$project": {"_id": 0, "hobby": 1}}
    ]

    result = db.hobbies.aggregate(pipeline)
    hobbies = list(result)
    hobbies_json = json.dumps(hobbies)

    return hobbies_json

# @app.get('/api/user_details/{username}', response_class=HTMLResponse)
# async def get_user_details(request: Request, username: str):
#     user = users_collection.find_one({"username": username})
#     if user:
#         user_details = {
#             "username": user.get("username"),
#             "email": user.get("email"),
#             "first_name": user.get("firstname"),
#             "last_name": user.get("lastname"),
#             "phone_number": user.get("phone_number"),
#             "full_address": user.get("full_address")
#         }
#         return JSONResponse(content=json.dumps(user_details))
#     else:
#         raise HTTPException(status_code=404, detail="User not found")

@app.get('/profile/{username}', response_class=HTMLResponse)
async def profile_page(request: Request, username: str):
    user = users_collection.find_one({"username": username})
    
    if user:
        hobbies = list(hobbies_collection.find({"user_id": str(user['_id'])}))
        context = {'request': request, 'user_name': user['username'], 'user_id': str(user['_id']), 'hobbies': hobbies}
        return templates.TemplateResponse('profile.html', context)
    else:
        raise HTTPException(status_code=404, detail="User not found")


def add_hobby_to_user(username: str, hobby: str):
    try:
        # Find the user document by username
        user_hobbies = hobbies_collection.find_one({"username": username})

        if not user_hobbies:
            raise HTTPException(status_code=404, detail=f"User with username {username} not found.")

        # Get the previous hobbies
        previous_hobbies = user_hobbies.get('hobbies', '')

        # Update the hobbies field
        new_hobbies = f"{previous_hobbies}, {hobby}" if previous_hobbies else hobby
        hobbies_collection.update_one(
            {"username": username},
            {user_hobbies['hobbies'].append(new_hobbies)}
        )
        
        print(f"Hobby '{hobby}' added successfully to user '{username}'.")
   
    except HTTPException as http_err:
        print(f"HTTP error occurred: {http_err.detail}")
   
    except Exception as err:
        print(f"An error occurred: {err}")

@app.get('/{username}/add_hobby', response_class=HTMLResponse)
async def add_hobby_form(request: Request, username: str):
    context = {'request': request, 'user_name': username}
    return templates.TemplateResponse('add_hobby.html', context)

@app.post('/{username}/hobbyAdd')
async def hobbyAdd(username: str, hobby: str = Form(...)):
    try:
        new_hobby = {"username": username, "hobby": hobby}
        result = db.hobbies.insert_one(new_hobby)
        
        if result.inserted_id:
            return {"message": "Hobby added successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to add hobby")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/api/hobbies/{username}/remove_hobby/{hobby}',response_class=HTMLResponse)
async def remove_hobby(request: Request, username: str, hobby:str):
    try:
        user = hobbies_collection.find_one_and_delete({"username": username, "hobby": hobby})
        return RedirectResponse(url=f"/profile/{username}", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get('/{username}/remove_hobbies', response_class=HTMLResponse)
async def remove_hobby_form(request: Request, username: str):
    context = {'request': request, 'user_name': username}
    return templates.TemplateResponse('remove_hobbies.html', context)


@app.get('/ADMIN', response_class=HTMLResponse)
async def admin(request: Request):
    context = {'request': request}
    return templates.TemplateResponse('admin.html', context)

@app.get('/ADMIN/view_logs', response_class=HTMLResponse)
async def view_logs(request: Request):
    with open('app.log', 'r') as f:
        logs = f.read()
    context = {'request': request, 'logs': logs}
    return templates.TemplateResponse('logs.html', context)

@app.get('/ADMIN/show_all_users', response_class=HTMLResponse)
async def show_all_users(request: Request):
    try:
        users = list(users_collection.find({}, {'_id': 0}))  # Do not include _id in the response
        context = {'request': request, 'users': users}
        return templates.TemplateResponse('show_all_users.html', context)
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error retrieving users: {err}")

@app.post('/ADMIN/add_user', response_class=HTMLResponse)
async def add_user(request: Request):
    try:
        data = await request.form()
        new_user = {
            'username': data['username'],
            'password': data['password'],
            'firstname': data['firstname'],
            'lastname': data['lastname'],
            'phone_number': data['phone_number'],
            'email': data['email'],
            'full_address': data['full_address'],
            'city': data['city'],
            'region': data['region'],
            'gender': data['gender'],
        }
        result = users_collection.insert_one(new_user)
        return RedirectResponse(url='/ADMIN/show_all_users', status_code=303)
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error adding user: {err}")

@app.get('/ADMIN/add_user', response_class=HTMLResponse)
async def add_user_form(request: Request):
    context = {'request': request}
    return templates.TemplateResponse('ADMIN_add_user.html', context)

@app.post('/delete_user/{username}')
async def delete_user(request: Request, username: str):
    try:
        result = users_collection.delete_one({'username': username})
        return RedirectResponse(url='/ADMIN/show_all_users', status_code=303)
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error deleting user: {err}")

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
    uvicorn.run(app, host="0.0.0.0", port=8000)
    