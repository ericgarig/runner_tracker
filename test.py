import unittest
from datetime import date
from flask.ext.testing import TestCase
from app import app, db
from app.models import Athlete, Workout, User


class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.create_all()
        db.session.add(User("usr", "pwd"))
        db.session.add(Athlete("John", "Doe"))
        db.session.add(Workout('1', date(2016, 1, 1)))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class FlaskTestCase(BaseTestCase):

    # Ensure that Flask was set up correctly
    def test_index(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that main page requires user login
    def test_main_route_requires_login(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertIn(b'Please Login', response.data)

    # Ensure that posts show up on the main page
    def test_athlete_list_after_login(self):
        response = self.client.post(
            '/login',
            data=dict(username="usr", password="pwd"),
            follow_redirects=True
        )
        self.assertIn(b'John Doe', response.data)



class UserViewsTests(BaseTestCase):
    
    # Ensure that the login page loads correctly
    def test_login_page_loads(self):
        response = self.client.get('/login')
        self.assertIn(b'Please Login', response.data)

    # Ensure login behaves correctly with correct credentials
    def test_correct_login(self):

        response = self.client.post(
            '/login',
            data=dict(username="usr", password="pwd"),
            follow_redirects=True
        )
        self.assertIn(b'You were logged in', response.data)

    # Ensure login behaves correctly with incorrect credentials
    def test_incorrect_login(self):
        response = self.client.post(
            '/login',
            data=dict(username="wrong", password="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'Invalid username or password.', response.data)

    # Ensure logout behaves correctly
    def test_logout(self):
        self.client.post(
            '/login',
            data=dict(username="usr", password="pwd"),
            follow_redirects=True
        )
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'You were logged out', response.data)



if __name__ == '__main__':
    unittest.main()
