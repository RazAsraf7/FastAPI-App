from fastapi import FastAPI, HTTPException
import json
import uvicorn
from person import Person
import re
import os

# Load existing users from new_users.json
new_users = {}
try:
    with open('new_users.json', 'r') as new_users_json:
        json_dict = json.load(new_users_json)
        for key, val in json_dict.items():
            new_users[int(key)] = val
except FileNotFoundError:
    print("new_users.json file not found")
except json.JSONDecodeError:
    print("Error decoding new_users.json")

# Create an in-memory dictionary of users
users_dictionary = {}
for key, val in new_users.items():
    users_dictionary[len(users_dictionary) + 1] = Person(**val)

# Function to convert Person object to dictionary
def person_to_dict(person: Person):
    return {
        'firstname': person.firstname,
        'lastname': person.lastname,
        'gender': person.gender,
        'phone_number': person.phone_number,
        'full_address': person.full_address,
        'hobbies': person.hobbies,
        'city': person.city,
        'region': person.region
    }

# Function to save user details to file
def save_user_details_to_file():
    try:
        with open('user_details.json', 'w') as user_details:
            json.dump([person_to_dict(v) for v in users_dictionary.values()], user_details, indent=4)
        print("user_details.json updated successfully")
    except Exception as e:
        print(f"Error saving to user_details.json: {e}")

# Write initial users to user_details.json
save_user_details_to_file()

app = FastAPI()

@app.get('/ADMIN/show_all_users')
async def show_all_users():
    return {"users": [person_to_dict(v) for v in users_dictionary.values()]}

@app.get('/available_people')
async def get_available_people():
    templist = []
    with open('user_details.json','r') as user_details_json:
        user_details = json.load(user_details_json)
    for user in user_details:
        if len(user['hobbies']) == 0:
            continue
        elif len(user['hobbies']) == 1:
            return f"{user['firstname']} enjoys {user['hobbies']}"
        else:
            templist.append(f"{user['firstname']} enjoys {' and '.join(user['hobbies'])}")
    return '\n'.join(templist)

@app.post('/register')
async def register(First_Name: str, Last_Name: str, User_Name: str, Password: str, Email: str, Address: str, City: str, Gender: str, Phone_Number: str):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", Email):
        raise HTTPException(status_code=400, detail='Email is not valid. Please try again')
    if not Password.isalnum():
        raise HTTPException(status_code=400, detail='Only letters and numbers are supported. (A-Z, a-z, 0-9)')
    if not User_Name.isidentifier():
        raise HTTPException(status_code=400, detail='User name must only contain letters, numbers, or underscores, and cannot start with a number.')

    user = {
        "firstname": First_Name,
        "lastname": Last_Name,
        "gender": Gender,
        "phone_number": Phone_Number,
        "full_address": f'{Address}, {City}',
        "hobbies": []
    }
    temp_user_dict = {'Username': User_Name, 'Password': Password, 'Email': Email}

    # Check if user already exists based on phone number
    for existing_user in users_dictionary.values():
        if existing_user.phone_number == Phone_Number:
            raise HTTPException(status_code=400, detail='User with this phone number already exists')

    # Load existing passwords
    try:
        if os.path.exists('users_passwords.json'):
            with open('users_passwords.json', 'r') as users_passwords_json:
                try:
                    users_passwords = json.load(users_passwords_json)
                except json.JSONDecodeError:
                    users_passwords = []
        else:
            users_passwords = []
    except Exception as e:
        print(f"Error loading users_passwords.json: {e}")

    users_passwords.append(temp_user_dict)
    
    # Save updated passwords
    try:
        with open('users_passwords.json', 'w') as users_passwords_json:
            json.dump(users_passwords, users_passwords_json, indent=4)
    except Exception as e:
        print(f"Error saving to users_passwords.json: {e}")

    # Add new user to dictionary
    try:
        person = Person(**user)
        users_dictionary[len(users_dictionary) + 1] = person
    except Exception as e:
        print(f"Error adding user to dictionary: {e}")

    # Save user details to file
    save_user_details_to_file()

    return f'Successfully created user {User_Name}'

@app.post('/login')
async def login(User_Name:str, Password:str, Email=None):
    with open('users_passwords.json', 'r') as user_password:
        users_passwords = json.load(user_password)
    for user in users_passwords:
        if User_Name == user['User_Name'] and Password == user['Password']:
            return f'{User_Name} successfully logged in'
        
        
if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=5500)
