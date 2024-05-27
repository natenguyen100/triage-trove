from models.models import User, Ticket, db
from app import app

db.drop_all()
db.create_all()

User.query.delete()
Ticket.query.delete()

Jon = User(first_name='Jon',
           last_name='Nguyen',
           username='jonny',
           email='jon100@gmail.com',
           password='flower123',
           confirm_password='flower123')

ticket = Ticket(subject='Test',
                description='Send help',
                priority='low',
                email='natenguyen100@gmail.com')

db.session.add(Jon)
db.session.add(ticket)
db.session.commit()