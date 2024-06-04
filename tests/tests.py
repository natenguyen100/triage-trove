import unittest
from app import app, db
from models.models import User, Ticket
from config import TestConfig

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('path.to.TestConfig')
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

class UserTests(BaseTestCase):
    def test_register_user(self):
        response = self.app.post('/register', data=dict(
            first_name='John',
            last_name='Doe',
            username='johndoe',
            email='john@example.com',
            password='password',
            confirm_password='password'
        ), follow_redirects=True)
        self.assertIn(b'Your account has been successfully created!', response.data)

    def test_login_user(self):
        self.app.post('/register', data=dict(
            first_name='John',
            last_name='Doe',
            username='johndoe',
            email='john@example.com',
            password='password',
            confirm_password='password'
        ), follow_redirects=True)
        
        response = self.app.post('/login', data=dict(
            username='johndoe',
            password='password'
        ), follow_redirects=True)
        self.assertIn(b'Welcome Back, johndoe!', response.data)

    def test_logout_user(self):
        self.app.post('/register', data=dict(
            first_name='John',
            last_name='Doe',
            username='johndoe',
            email='john@example.com',
            password='password',
            confirm_password='password'
        ), follow_redirects=True)
        self.app.post('/login', data=dict(
            username='johndoe',
            password='password'
        ), follow_redirects=True)
        
        response = self.app.get('/logout', follow_redirects=True)
        self.assertIn(b'Login', response.data)

class TicketTests(BaseTestCase):
    def test_create_ticket(self):
        response = self.app.post('/ticket_submission', data=dict(
            subject='Test Ticket',
            description='This is a test ticket.',
            priority='High',
            email='john@example.com'
        ), follow_redirects=True)
        self.assertIn(b'Ticket submitted', response.data)
    
    def test_assign_ticket(self):
        self.app.post('/register', data=dict(
            first_name='John',
            last_name='Doe',
            username='johndoe',
            email='john@example.com',
            password='password',
            confirm_password='password'
        ), follow_redirects=True)
        self.app.post('/login', data=dict(
            username='johndoe',
            password='password'
        ), follow_redirects=True)

        self.app.post('/ticket_submission', data=dict(
            subject='Test Ticket',
            description='This is a test ticket.',
            priority='High',
            email='john@example.com'
        ), follow_redirects=True)
        
        ticket = Ticket.query.first()
        response = self.app.post(f'/assign_ticket/{ticket.id}', follow_redirects=True)
        self.assertIn(b'Ticket assigned to you successfully!', response.data)

    def test_delete_ticket(self):
        self.app.post('/register', data=dict(
            first_name='John',
            last_name='Doe',
            username='johndoe',
            email='john@example.com',
            password='password',
            confirm_password='password'
        ), follow_redirects=True)
        self.app.post('/login', data=dict(
            username='johndoe',
            password='password'
        ), follow_redirects=True)

        self.app.post('/ticket_submission', data=dict(
            subject='Test Ticket',
            description='This is a test ticket.',
            priority='High',
            email='john@example.com'
        ), follow_redirects=True)
        
        ticket = Ticket.query.first()
        response = self.app.post(f'/delete_ticket/{ticket.id}', follow_redirects=True)
        self.assertIn(b'Ticket deleted successfully!', response.data)

if __name__ == '__main__':
    unittest.main()