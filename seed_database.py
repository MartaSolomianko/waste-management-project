"""Script to drop and reseed database for waste management app."""

import os
import csv
from random import choice, uniform
from datetime import datetime, date
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
        #weight is a string
        if item["weight"] == "":
            item["weight"] = 0
        weight = item["weight"]
        #weight needs to be a float
        weight = float(weight)

        # changes the value of rinse to a boolean
        if item["rinse"] == 'f':
            item["rinse"] = False
        item["rinse"] = True

        # captures the new Boolean value for rinse
        rinse = item["rinse"]

        # captures the value for special_instructions as a string
        special_instructions = item["special_instructions"]

        # makes items for my database out of the values captured from my CSV
        db_item = crud.create_item(bin_type, name, material, weight, rinse, special_instructions)
        items_in_db.append(db_item)

# adds the item objects to the database and commits them to the items table.         
model.db.session.add_all(items_in_db)
model.db.session.commit()
  


############### Make a user in my database table user and a history of records for that user ############
ph = PasswordHasher()

name = "Marta"
email = "marta@gmail.com"
password = "test"
hashed_pw = ph.hash(password)
user = crud.create_user(email, hashed_pw, name)
model.db.session.add(user)

# random ordered lists of days 
sept_days = [2, 5, 6, 9, 14, 16, 19, 22, 24, 26, 28]
oct_days = [1, 3, 4, 5, 8, 10, 12, 14, 18, 19, 22]
nov_days = [1, 4, 7, 8, 10, 13, 15]

db_dict = {}

db_dict[9] = sept_days
db_dict[10] = oct_days
db_dict[11] = nov_days

for month in db_dict:
    month = month
    for days in db_dict[month]:
        day = days
        date_time = date(2022,month,day)
        random_bin = choice(bin_type_list)
        weight = uniform(1, 20)
        weight = round(weight, 2)

        # make and add september records to db
        record = crud.create_record(user, random_bin, date_time, weight)
        model.db.session.add(record)


model.db.session.commit()
