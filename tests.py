import unittest

from server import app
from model import db, connect_to_db, example_data

class WasteManagmentTests(unittest.TestCase):
    """Tests for waste management site."""

    def setUp(self):
        """Setup before every test."""

        # get the Flask test client
        self.client = app.test_client()

        # show Flask errors that happen during tests
        app.config['TESTING'] = True


    def test_homepage(self):
        """Test the homepage route."""
        result = self.client.get("/")

        # testing that if you are at the homepage, you see the Login/Regester 
        self.assertIn(b"Don't have an account?", result.data)


    
class WasteManagmentTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Setup before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    
    def test_login(self):
        """Test user login."""

        login = self.client.post("/login", data={"email": "marta2@test.com", "password": "test"}, follow_redirects=True)
        self.assertIn(b"Welcome back, Marta", login.data)
        self.assertNotIn(b"Don't have an account?", login.data)


    def tearDown(self):
        """Tear down at the end of every test."""

        db.session.close()
        db.drop_all()


if __name__ == "__main__":
    unittest.main()
