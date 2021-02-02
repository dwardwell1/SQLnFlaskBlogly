from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="Test",last_name="User", image_url="https://scontent-sjc3-1.xx.fbcdn.net/v/t1.0-0/s640x640/144700196_10225818786558398_3770794163187827306_n.jpg?_nc_cat=107&ccb=2&_nc_sid=8bfeb9&_nc_ohc=nheSEZH-Uc8AX-MuJWi&_nc_ht=scontent-sjc3-1.xx&tp=7&oh=b9ce323143aed328a85897e540aa79bf&oe=603D0CBF")
        db.session.add(user)
        db.session.commit()

        self.id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()
    
    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test', html)
    
    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<h1>Hello User</h1>', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"firstName": "TestUser2", "lastName": "Second", "imgURL": "https://images.unsplash.com/photo-1593642532871-8b12e02d091c?ixid=MXwxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1300&q=80"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestUser2", html)

    def test_edit_user(self):
        with app.test_client() as client:
            d = {"firstName": "alt1", "lastName": "third", "imgURL": "https://images.unsplash.com/photo-1593642532871-8b12e02d091c?ixid=MXwxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1300&q=80"}
            resp = client.post(f"/users/{self.id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("alt1", html)
