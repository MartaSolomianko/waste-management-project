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
    """Return a user by email, returns None if not foundqu."""

    return User.query.filter(User.email == email).first()



def create_record(user, bin_type, date_time, weight):
    """Create and return a new record."""

    record = Record(user=user, bin_type_code=bin_type, date_time=date_time, weight=weight)

    return record



def create_item(bin_type, name, material, rinse, special_instructions):
    """Create and return a new item."""

    # I had mistakenly written bin_type=bin_type instead of bin_type_code=bin_type
    # need bin_type_code because I am working with a string and NOT an binType object
    item = Item(bin_type_code=bin_type, name=name, material=material, rinse=rinse, special_instructions=special_instructions)

    return item



def create_bin_type(type_code):
    """Create and return a new bin type."""

    bintype = BinType(type_code=type_code)

    return bintype



#######################################################################

if __name__ == "__main__":
    from server import app

    connect_to_db(app)
