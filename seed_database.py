"""Script to seed database for waste management app."""

import os
import csv
from random import choice, uniform
from datetime import datetime
from argon2 import PasswordHasher

import crud
import model
import server

os.system("dropdb waste_db")
os.system("createdb waste_db")

model.connect_to_db(server.app)
model.db.create_all()


####### Make bin_types in my database table bin_types ###################################

bin_type_list = ["R", "T", "C", "H"]

for bin in bin_type_list:
    bin_type = crud.create_bin_type(bin)
    model.db.session.add(bin_type)

model.db.session.commit()



######## Make items in my database table items ##########################################

with open("data/items.csv", newline="") as csv_file:
    items = csv.DictReader(csv_file)
    # items is a dictionary object
    #print(items)
    
    # items_in_db is a list of dictionaries. 
    # Each dictionary in the list contains the values for an item in my db
    items_in_db = []

    # separate out the dictionary object into key: value pairs
    # I want each line in my CSV file to become a separate item in my database, aka row. 
    for item in items:

        #bin_type is a string
        bin_type = item["bin_type_code"]
        #name is a string
        name = item["name"]
        #material is a string
        material = item["material"]

        # changes the value of rinse to a boolean
        if item["rinse"] == 'f':
            item["rinse"] = False
        item["rinse"] = True

        # captures the new Boolean value for rinse
        rinse = item["rinse"]

        # captures the value for special_instructions as a string
        special_instructions = item["special_instructions"]

        # makes items for my database out of the values captured from my CSV
        db_item = crud.create_item(bin_type, name, material, rinse, special_instructions)
        items_in_db.append(db_item)

# adds the item objects to the database and commits them to the items table.         
model.db.session.add_all(items_in_db)
model.db.session.commit()
  


############### Make users in my database table user, each user will make 2 records ####
ph = PasswordHasher()
names = ["Daniela", "Sherese", "Dan", "Rochelle", "Leslie", "Ozan", "Xenia", "Emily", "Monica", "Javier"]

for n in range(10):
    email = f"user{n}@test.com" 
    password = "test"
    for name in names:
        name = f"{names[n]}"

    hashed_pw = ph.hash(password)
    user = crud.create_user(email, hashed_pw, name)
    model.db.session.add(user)

    for _ in range(2):
        random_bin = choice(bin_type_list)
        weight = uniform(1, 20)
        date_time = datetime.now()

        record = crud.create_record(user, random_bin, date_time, weight)
        model.db.session.add(record)

model.db.session.commit()



#Q1 
#### Normally when a user records a weight of their trash, they will submit a form
#### can that form be submitted with a datetime.now() stamp so the user doesn't have 
#### to enter the day and time each time they submit a record in their form?


#Q2 
#### two columns in my items table have default values at the database level.
#### do those defaults come into play if I were to have an empty value for 
#### them in my CSV data? 