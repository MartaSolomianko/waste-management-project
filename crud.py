"""CRUD operations for waste management app."""

from model import db, User, Record, Item, BinType, connect_to_db
from datetime import datetime


def create_user(email, password, name):
    """Create and return a new user."""

    user = User(email=email, password=password, name=name)

    return user



def get_user_by_id(user_id):
    """Return a user by their ID, returns None if not found"""

    return User.query.get(user_id)



def get_user_by_email(email):
    """Return a user by email, returns None if not found."""

    return User.query.filter(User.email == email).first()



def create_record(user, bin_type, date_time, weight):
    """Create and return a new record."""

    record = Record(user_id=user, bin_type_code=bin_type, date_time=date_time, weight=weight)

    return record



def get_records_by_user_id(user_id):
    """Return a list of records by user_id."""

    records = db.session.query(Record).filter(Record.user_id == user_id).all()

    return records



def get_record_by_record_id(record_id):
    """Return a specific record by record_id."""

    record = db.session.query(Record).filter(Record.record_id == record_id).first()

    return record



def create_item(bin_type, name, material, weight, rinse, special_instructions):
    """Create and return a new item."""

    item = Item(bin_type_code=bin_type, name=name, material=material, weight=weight, rinse=rinse, special_instructions=special_instructions)

    return item



def get_item_by_name(name):
    """Return an item by name, else returns None."""
    
    return db.session.query(Item).filter(Item.name == f"{name}").first() 



def get_similar_item_by_name(name):
    """Return an item that is realted to a searched name"""

    item = db.session.query(Item).filter(Item.name.like(f"%{name}%")).first()

    if not item:
        word_list = name.split() # returns a list of strings, original word was split at spaces
        for word in word_list:
            item = db.session.query(Item).filter(Item.name.like(f"%{word}%")).first()
            if item:
                return item
            
    return item



def get_item_by_material(material):
    """Return an item based on material."""

    return db.session.query(Item).filter(Item.material == f"{material}").first()



def get_similar_item_by_material(material):
    """Return an item by material."""

    return db.session.query(Item).filter(Item.material.like(f"%{material}%")).first()



def create_bin_type(type_code):
    """Create and return a new bin type."""

    bintype = BinType(type_code=type_code)

    return bintype



def clean_user_search(user_search):
    """Returns a lowercased, punctuation-free, and right-side-space-free string."""

    formatted_string = ""
    punctuation = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    
    string = user_search.lower().rstrip()

    for element in string:
        if element not in punctuation:
            formatted_string+=element

    return formatted_string



#######################################################################

if __name__ == "__main__":
    from server import app

    connect_to_db(app)
