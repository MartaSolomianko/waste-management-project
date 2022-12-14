"""Models for waste management app."""

from flask_sqlalchemy import SQLAlchemy
from argon2 import PasswordHasher
from datetime import date


db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    records = db.relationship("Record", back_populates="user")
    
    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"
    

    
class Record(db.Model):
    """A waste record."""

    __tablename__ = "records"

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date_time = db.Column(db.Date, nullable=False) 
    weight = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    bin_type_code = db.Column(db.String(5), db.ForeignKey("bin_types.type_code"), nullable=False)

    user = db.relationship("User", back_populates="records")
    bin_type = db.relationship("BinType", back_populates="records")

    def __repr__(self):
        return f"<Record record_id={self.record_id} date_time={self.date_time} bin_type_code={self.bin_type_code}>"
    


class Item(db.Model):
    """An item."""

    __tablename__ = "items"

    item_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    material = db.Column(db.String(100), nullable=True)
    weight = db.Column(db.Float, nullable=False)
    rinse = db.Column(db.Boolean, default=False)
    special_instructions = db.Column(db.Text, default=None)
    bin_type_code = db.Column(db.String(5), db.ForeignKey("bin_types.type_code"), nullable=False)

    bin_type = db.relationship("BinType", back_populates="items")

    def __repr__(self):
        return f"<Item item_id={self.item_id} name={self.name} bin_type_code={self.bin_type_code}>"
    


class BinType(db.Model):
    """A bin type."""

    __tablename__ = "bin_types"

    type_code = db.Column(db.String(5), primary_key=True)

    records = db.relationship("Record", back_populates="bin_type")
    items = db.relationship("Item", back_populates="bin_type")

    def __repr__(self):
        return f"<BinType type_code={self.type_code}>"


############################ TESTING AND DB CONNECTIONS ########################
def connect_to_db(flask_app, db_uri="postgresql:///waste_db", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


def example_data():
    """Example data for test database."""

    ph = PasswordHasher()

    testuser = User(user_id=10, name="Marta", email="marta2@test.com", password=ph.hash("test"))
    testbin = BinType(type_code="R")
    testrecord = Record(record_id=100, user_id=testuser.user_id, bin_type_code="R", weight=5, date_time=date(2022,11,18))

    db.session.add(testuser)
    db.session.add(testbin)
    db.session.add(testrecord)
    db.session.commit()



if __name__ == "__main__":
    from server import app

    connect_to_db(app)