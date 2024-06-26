from flask import Flask, render_template, redirect, session, url_for, flash, request, abort
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import current_user
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from models.models import *
from forms.user_form import *
from forms.ticket_form import *
from forms.profile_form import *
import config

app = Flask(__name__)
CORS(app)
app.config.from_object(config.Config)

connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.context_processor
def inject_user():
    return dict(user=current_user)

@app.route("/")
def login_page():
    """Login page"""
    return redirect('/login')

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user"""
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        existing_user = User.query.filter_by(email=email).first()
        
        if existing_user:
            flash("Email already taken. Please use a different email address.", "error")
            return render_template('users/register.html', form=form)

        user = User.register(first_name=form.first_name.data,
                             last_name=form.last_name.data,
                             username=form.username.data,
                             email=form.email.data,
                             password=form.password.data,
                             confirm_password=form.confirm_password.data)
        db.session.add(user)
        db.session.commit()
        session['username'] = user.username
        flash("Your account has been successfully created!", "success")
        return redirect(url_for('register'))
    return render_template('users/register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login user"""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(username=form.username.data, password=form.password.data)
        if user:
            flash(f"Welcome Back, {user.username}!")
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            form.username.errors = ['Invalid username or password.']
    return render_template('users/login.html', form=form)

@app.route('/logout')
def logout():
    """Logout user"""
    session.pop("user_id")
    return redirect(url_for('login'))

def get_user_by_session():
    """Retrieve the user from the session."""
    if 'user_id' not in session:
        flash("You need to log in first.")
        return None
    return User.query.get_or_404(session['user_id'])

def get_ticket_by_id(ticket_id):
    """Retrieve a ticket by its ID."""
    return Ticket.query.get_or_404(ticket_id)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    """Ticket dashboard"""
    if request.method == 'POST':
        user = User.authenticate(request.form['username'], request.form['password'])
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials")
            return redirect(url_for('login_page'))
    else:
        user = get_user_by_session()
        if user:
            all_tickets = Ticket.query.all()
            assigned_tickets = Ticket.query.filter_by(user_id=user.id).all()
            return render_template('tickets/ticket_dashboard.html', user=user, tickets=all_tickets, assigned_tickets=assigned_tickets)
        return redirect(url_for('login_page'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """Profile page"""
    user = get_user_by_session()
    if not user:
        return redirect(url_for('login_page'))

    form = ProfileForm(obj=user)

    if request.method == 'POST' and form.validate_on_submit():
        new_username = form.username.data
        existing_user = User.query.filter(User.username == new_username, User.id != user.id).first()
        
        if existing_user:
            flash('Username already taken. Please choose a different username.', 'error')
            return render_template('users/profile.html', form=form, user=user)
        
        user.username = new_username
        user.email = form.email.data
        user.role = form.role.data
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('users/profile.html', form=form, user=user)


@app.route('/ticket_submission', methods=['GET', 'POST'])
def ticket_submission():
    """Submitting a Ticket"""
    form = TicketForm()
    if form.validate_on_submit():
        new_ticket = Ticket(
            subject=form.subject.data,
            description=form.description.data,
            priority=form.priority.data,
            email=form.email.data
        )
        db.session.add(new_ticket)
        db.session.commit()
        return redirect(url_for('ticket_submitted'))
    return render_template('tickets/ticket_form.html', form=form)

@app.route('/ticket_submitted')
def ticket_submitted():
    """Submitted a Ticket"""
    return render_template('/tickets/ticket_submitted.html')

@app.route('/assign_ticket/<int:ticket_id>', methods=['POST'])
def assign_ticket(ticket_id):
    """Assign a ticket to the logged-in user."""
    user = get_user_by_session()
    if not user:
        return redirect(url_for('login'))

    ticket = get_ticket_by_id(ticket_id)

    if ticket.user_id is None:
        ticket.user_id = user.id
        db.session.commit()
        flash("Ticket assigned to you successfully!")
    else:
        flash("This ticket is already assigned.")

    return redirect(url_for('dashboard'))

@app.route('/unassign_ticket/<int:ticket_id>', methods=['POST'])
def unassign_ticket(ticket_id):
    """Unassign a ticket from the user."""
    user = get_user_by_session()
    if not user:
        return redirect(url_for('login'))

    ticket = get_ticket_by_id(ticket_id)

    if ticket.user_id == user.id:
        ticket.user_id = None
        db.session.commit()
        flash("Ticket unassigned successfully!")
    else:
        flash("You can only unassign tickets assigned to yourself.")

    return redirect(url_for('dashboard'))

@app.route('/delete_ticket/<int:ticket_id>', methods=['POST'])
def delete_ticket(ticket_id):
    """Delete a ticket."""
    user = get_user_by_session()
    if not user:
        return redirect(url_for('login'))

    ticket = get_ticket_by_id(ticket_id)

    if ticket.user_id == user.id:
        db.session.delete(ticket)
        db.session.commit()
        flash("Ticket deleted successfully!")
    else:
        flash("You can only delete tickets assigned to yourself.")

    return redirect(url_for('dashboard'))
