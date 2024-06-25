from pymongo import MongoClient

# MongoDB connection URI
uri = "mongodb+srv://raz:F4vy5JzhUg@dmd.hjdhwf6.mongodb.net/DMD?retryWrites=true&w=majority"

# Connect to MongoDB
client = MongoClient(uri)

# Access database and collection
db = client['DMD']
users_collection = db['users']

# Fetch city-district mappings from MongoDB
def fetch_city_district_mappings():
    cursor = db['city_district']
    results = cursor.find({})
    city_district_map = {}
    for result in results:
        city_district_map[result['city']] = result['district']
    return city_district_map

# Define the Person class with MongoDB integration
class Person:
    def __init__(self, firstname: str, lastname: str, phone_number: str, full_address: str, gender: str, hobbies=None):
        self.firstname = firstname
        self.lastname = lastname
        self.name = f'{self.firstname} {self.lastname}'
        self.gender = gender
        self.phone_number = phone_number
        self.full_address = full_address
        self.hobbies = hobbies or []
        self.city = self.determine_city()
        self.region = self.determine_region()
        self.save_to_db()

    def determine_city(self) -> str:
        address_parts = self.full_address.split(', ')
        potential_city = address_parts[-1]
        return potential_city if potential_city in city_district_map else 'unknown'

    def determine_region(self) -> str:
        return city_district_map.get(self.city, 'unknown')

    def save_to_db(self):
        hobbies_str = ', '.join(self.hobbies)
        user_data = {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "full_name": self.name,
            "gender": self.gender,
            "phone_number": self.phone_number,
            "full_address": self.full_address,
            "city": self.city,
            "region": self.region,
            "hobbies": hobbies_str.lower()
        }
        users_collection.insert_one(user_data)

    def add_hobby(self, hobby: str):
        self.hobbies.append(hobby)
        self.sort_hobbies()
        self.save_to_db()

    def sort_hobbies(self):
        self.hobbies.sort()

    def matchmaking(self):
        self.nearby_people = users_collection.find({"city": self.city, "full_name": {"$ne": self.name}})
        self.matching_people = []

        for person in self.nearby_people:
            if any(hobby in self.hobbies for hobby in person["hobbies"].split(", ")):
                self.matching_people.append(person["full_name"])

        if self.matching_people:
            return f'{", ".join(self.matching_people)} are your matches. You can now contact them!'
        else:
            return f'Unfortunately, no matches were found in {self.city} or {self.region}.'

    def contact_matches(self):
        matching_people = users_collection.find({"full_name": {"$in": self.matching_people}})
        contact_info = [f'{person["full_name"]}\'s phone number is: 0{person["phone_number"]}' for person in matching_people]
        return '\n'.join(contact_info) if contact_info else 'Unfortunately, there are no matches.'

    def info(self):
        return f'Here is all the information we know about you:\nYour name is {self.firstname} {self.lastname},\n You are living at {self.full_address},\nYour phone number is {self.phone_number}'

# Fetch city-district mappings from MongoDB
city_district_map = fetch_city_district_mappings()

# # Sample usage of Person class
# person1 = Person("John", "Doe", "123456789", "123 Main St, Tel Aviv", "Male", hobbies=["Reading", "Cooking"])
# print(person1.matchmaking())
# print(person1.info())

# Close MongoDB connection
client.close()
