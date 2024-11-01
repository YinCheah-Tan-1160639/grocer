from flask import Blueprint, render_template, abort, request, redirect, url_for, session, flash
from decorators import role_required
from models import Person

from app import db
from app import hashing

store_bp = Blueprint("store", __name__)

@store_bp.route("/")
def index():    
    # Check if has session
    if "username" not in session or "role" not in session:
        return render_template('index.html')
    return render_template("index.html",
                           role=session['role'],
                           username=session['username'])

@store_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("auth.html")
    else:
        try:
            # get user input
            username = request.form.get('username')
            password = request.form.get('password')

            user = Person.query.filter_by(username=username).first()
                    
            if user and hashing.check_value(user.password, password, salt='abcd'):
                session['user_id'] = user.id  # Store user ID in session
                session['role'] = user.type  # Store user role in session
                session['username'] = user.username # Store username in session
                flash('You were successfully logged in!', 'success')
                return redirect(url_for('store.dashboard'))
            else:
                flash('Invalid username or password!', 'error')
                return redirect(url_for('store.login'))
        except Exception:
            flash('An error occurred while trying to log in. Please try again later.', 'error')
            return redirect(url_for('store.login'))


@store_bp.route("/dashboard")
@role_required('staff', 'customer', 'corporate_customer')
def dashboard():
    return render_template("dashboard.html", 
                           role=session['role'],
                           username=session['username'])

@store_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('store.login'))