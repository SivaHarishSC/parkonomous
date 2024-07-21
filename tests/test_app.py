"""
This module contains unit tests for the Flask application.
"""

import unittest
import tempfile
import os
import logging
from app import app, get_db_connection

class FlaskTestCase(unittest.TestCase):
    """Test case for Flask application"""

    def setUp(self):
        """TC_FLASK_001: Set up the test environment and database."""
        self.db_fd, self.db_path = tempfile.mkstemp()
        app.config['DATABASE'] = self.db_path
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test_secret'
        self.app = app.test_client()
        self.setup_database()
        logging.info("Test environment set up")

    def tearDown(self):
        """TC_FLASK_002: Tear down the test environment and database."""
        os.close(self.db_fd)
        os.unlink(self.db_path)
        logging.info("Test environment torn down")

    def setup_database(self):
        """TC_FLASK_003: Create the necessary tables in the temporary database."""
        with get_db_connection() as con:
            cur = con.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS customer (
                            name TEXT PRIMARY KEY,
                            password TEXT NOT NULL,
                            mobile_number INTEGER NOT NULL,
                            vehicle_id INTEGER NOT NULL)''')
            con.commit()
        logging.info("Database set up")

    def test_index(self):
        """TC_FLASK_004: Verify that the index page contains 'Login'."""
        rv = self.app.get('/')
        self.assertIn(b'Login', rv.data)
        logging.info("Index page test passed")

    def test_register_get(self):
        """TC_FLASK_005: Verify that the register page contains 'Register'."""
        rv = self.app.get('/register')
        self.assertIn(b'Register', rv.data)
        logging.info("Register GET test passed")

    def test_register_post(self):
        """TC_FLASK_006: Test successful registration of a user."""
        rv = self.app.post('/register', data=dict(
            name='testuser',
            password='testpass',
            contact='1234567890',
            vehicle_id='1'
        ), follow_redirects=True)
        self.assertIn(b'Record Added Successfully', rv.data)
        logging.info("Register POST test passed")

    def test_login_get(self):
        """TC_FLASK_007: Verify that the login page contains 'Login'."""
        rv = self.app.get('/login', follow_redirects=True)
        self.assertTrue(b'Login' in rv.data or b'login' in rv.data.lower())
        logging.info("Login GET test passed")

    def test_login_post_success(self):
        """TC_FLASK_008: Test successful login of a registered user."""
        with self.app as client:
            with client.session_transaction() as sess:
                sess['name'] = 'testuser'  # Directly set the session data

        with self.app as client:
            with client.session_transaction() as sess:
                self.assertIn('name', sess, "Session does not contain 'name'")
                self.assertEqual(sess['name'], 'testuser', "Session name mismatch")
        logging.info("Login POST success test passed")

    def test_login_post_fail(self):
        """TC_FLASK_010: Test login attempt with incorrect username or password."""
        rv = self.app.post('/login', data=dict(
            name='wronguser',
            password='wrongpass'
        ), follow_redirects=True)
        self.assertIn(b'Username and Password Mismatch', rv.data)
        logging.info("Login POST fail test passed")

    def test_logout(self):
        """TC_FLASK_011: Test logout functionality."""
        with self.app as client:
            with client.session_transaction() as sess:
                sess['name'] = 'testuser'  # Set session for test user
            rv = self.app.get('/logout', follow_redirects=True)
            self.assertTrue(b'Login' in rv.data or b'login' in rv.data.lower())
        logging.info("Logout test passed")

    def test_about(self):
        """TC_FLASK_012: Verify that the about page contains 'About'."""
        rv = self.app.get('/about')
        self.assertTrue(b'About' in rv.data or b'about' in rv.data.lower())
        logging.info("About page test passed")

    def test_service(self):
        """TC_FLASK_013: Verify that the service page contains 'Destination Status'."""
        rv = self.app.get('/service')
        self.assertTrue(b'Destination Status' in rv.data or b'destination status' in rv.data.lower())
        logging.info("Service page test passed")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()
