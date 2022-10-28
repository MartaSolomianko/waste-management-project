"""CRUD operations for waste management app."""

from model import db, User, Record, Item, BinType, connect_to_db


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user



def get_user_by_id(user_id):
    """Return a user by their ID, returns None if not found"""

    return User.query.get(user_id)



def get_user_by_email(email):
    """Return a user by email, returns None if not found."""

    return User.query.filter(User.email == email).first()



def create_record(user, bin_type, date_time, weight):
    """Create and return a new record."""

    record = Record(user=user, bin_type_code=bin_type, date_time=date_time, weight=weight)

    return record



def create_item(bin_type, name, material, rinse, special_instructions):
    """Create and return a new item."""

    item = Item(bin_type_code=bin_type, name=name, material=material, rinse=rinse, special_instructions=special_instructions)

    return item



def get_item_by_name(name):
    """Return an item by name, else returns None."""

    return db.session.query(Item).filter(Item.name == f"{name}").first() 



def get_similar_item_by_name(name):
    """Return an item that is realted to a searched name"""

    return db.session.query(Item).filter(Item.name.like(f"%{name}%")).first()



def get_item_by_material(material):
    """Return an item based on material."""

    return db.session.query(Item).filter(Item.material == f"{material}").first()



def get_similar_item_by_material(material):
    """Return an item by material."""

    return db.session.query(Item).filter(Item.material.like(f"%{material}%")).first()



# def get_items_by_bin_type(bin_type_code):
#     """Return an item by bin type."""

#     return db.session.query(Item).filter(Item.bin_type_code == f"{bin_type_code}").all()



def create_bin_type(type_code):
    """Create and return a new bin type."""

    bintype = BinType(type_code=type_code)

    return bintype



def clean_user_search(user_search):
    """Returns a lowercased, punctuation-free, and space-free string."""

    formatted_string = ""
    punctuation = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    
    string = user_search.lower().strip()

    for element in string:
        if element not in punctuation:
            formatted_string+=element

    return formatted_string



def check_search_not_empty(user_search):
    """Returns None if user search is empty."""

    if user_search == " ":
        return None
    return user_search 



#######################################################################

if __name__ == "__main__":
    from server import app

    connect_to_db(app)
