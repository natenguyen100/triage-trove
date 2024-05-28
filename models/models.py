from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    with app.app_context():
        db.app = app
        db.init_app(app)
        db.create_all()

user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String,
                           nullable=False)
    
    last_name = db.Column(db.String,
                          nullable=False)
    
    username = db.Column(db.String,
                         nullable=False,
                         unique=True)
    
    email = db.Column(db.String,
                      nullable=False,
                      unique=True)
    
    password = db.Column(db.String,
                         nullable=False,
                         unique=True)
    
    confirm_password = db.Column(db.String,
                                 nullable=False,
                                 unique=True)
    
    roles = db.relationship('Role', secondary=user_roles, backref='users')

    @classmethod
    def register(cls, first_name, last_name, username, email, password, confirm_password):
        """Register user with hashed password & return user"""
    
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(first_name=first_name, last_name=last_name, username=username, email=email, password=hashed_utf8, confirm_password=hashed_utf8)
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """validate that user & password"""

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True)
    
    role_name = db.Column(db.String,
                          nullable=True,
                          unique=True)
        
class Ticket(db.Model):
    __tablename__ = 'tickets'


    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    subject = db.Column(db.Text,
                           nullable=False)
    
    description = db.Column(db.Text,
                            nullable=False)
    
    priority = db.Column(db.String,
                         nullable=False)
    
    email = db.Column(db.String,
                      nullable=True)
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=True)

    user = db.relationship('User', backref='tickets')

    def ticket_post(self):
        ticket = {'subject': self.subject.data, 'description': self.description, 'priority': self.priority, 'email': self.email}