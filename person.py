import mysql.connector

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    port=3307,  # Use port 3307 if MySQL is running on this port
    user="raz",
    password="123456",
    database="DMD_users"
)

cursor = db.cursor()

def fetch_city_district_mappings():
    cursor.execute("SELECT name, region FROM Cities")
    results = cursor.fetchall()
    city_district_map = {}
    for city, district in results:
        city_district_map[city] = district
    return city_district_map

city_district_map = fetch_city_district_mappings()

person_hobbies = {}
persons_cities = {}
persons_regions = {}
person_phone_number = {}

# Define the Person class with database integration
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
        persons_cities.setdefault(self.city, []).append(self.name)
        person_phone_number[self.name] = self.phone_number
        self.region = self.determine_region()
        persons_regions.setdefault(self.region, []).append(self.name)
        self.save_to_db()

    def determine_city(self) -> str:
        address_parts = self.full_address.split(', ')
        potential_city = address_parts[-1]
        return potential_city if potential_city in city_district_map else 'unknown'

    def determine_region(self) -> str:
        return city_district_map.get(self.city, 'unknown')

    def save_to_db(self):
        hobbies_str = ', '.join(self.hobbies)
        cursor.execute(
            "INSERT INTO hobbies (firstname, lastname, full_name, phone_number, city, region, hobbies) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s) "
            "ON DUPLICATE KEY UPDATE firstname=VALUES(firstname), lastname=VALUES(lastname), "
            "phone_number=VALUES(phone_number), city=VALUES(city), region=VALUES(region), hobbies=VALUES(hobbies)",
            (self.firstname, self.lastname, self.name, self.phone_number, self.city, self.region, hobbies_str.lower())
        )

        cursor.execute(
            "INSERT INTO users (firstname, lastname, full_name, gender, phone_number, full_address, city, region) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (self.firstname, self.lastname, self.name, self.gender, self.phone_number, self.full_address, self.city, self.region)
        )

        db.commit()

    def add_hobby(self, hobby: str, rating: int):
        self.hobbies.append(hobby)
        person_hobbies.setdefault(hobby, []).append(self.name)
        self.sort_hobbies()

    def sort_hobbies(self):
        self.hobbies.sort()

    def matchmaking(self):
        self.nearby_people = [p for p in persons_cities.get(self.city, []) if p != self.name]
        self.matching_people = []

        if self.nearby_people:
            for hobby in self.hobbies:
                if hobby in person_hobbies:
                    for p in person_hobbies[hobby]:
                        if p != self.name and p in self.nearby_people:
                            self.matching_people.append(p)
            if self.matching_people:
                return f'{", ".join(self.matching_people)} are your matches. You can now contact them!'
        else:
            regional_people = [p for p in persons_regions.get(self.region, []) if p != self.name]
            if regional_people:
                for hobby in self.hobbies:
                    if hobby in person_hobbies:
                        for p in person_hobbies[hobby]:
                            if p in regional_people:
                                self.matching_people.append(p)
                if self.matching_people:
                    return f'{", ".join(self.matching_people)} are your regional matches. You can now contact them!'
            print(f'Unfortunately, no matches were found in {self.city} or {self.region}.')
            all_country_search = input('Would you like to search for people in farther places?')
            if 'n' in all_country_search.lower():
                return 'Understood. Maybe next time!'
            else:
                for hobby in person_hobbies.keys():
                    if hobby in self.hobbies:
                        print("There might be someone in your country who shares the same hobbies!")
                        for person in person_hobbies[hobby]:
                            if person != self.name and person not in self.matching_people:
                                self.matching_people.append(person)
                                return f'{person} is a match for you!'
            if len(self.matching_people) == 0:
                return 'Unfortunately, we couldn\'t find anyone with the same hobbies as you.'

    def contact_matches(self):
        if self.matching_people:
            contact_info = [f'{matcher}\'s phone number is: 0{person_phone_number[matcher]}' for matcher in self.matching_people]
            return '\n'.join(contact_info)
        else:
            return 'Unfortunately, there are no matches.'

    def info(self):
        return f'Here is all the information we know about you:\nYour name is {self.firstname} {self.lastname}, You are living at {self.full_address},\nYour phone number is {self.phone_number}'

# Load existing users from new_users.json
# new_users = {}
# with open('new_users.json', 'r') as new_users_json:
#     json_dict = json.load(new_users_json)
#     for key, val in json_dict.items():
#         new_users[int(key)] = val

# Create an in-memory dictionary of users
# users_dictionary = {}
# for key, val in new_users.items():
#     users_dictionary[len(users_dictionary) + 1] = Person(**val)
