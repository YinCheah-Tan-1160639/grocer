from flask import Blueprint, render_template, abort, request, redirect, url_for, session, flash
from models import Person

store_bp = Blueprint('store', __name__)

@store_bp.route("/")
def index():    
    # check if has session
    # if 'username' not in session or 'role' not in session:
    #     return render_template('index.html', events=events, latest_news=latest_news_data)

    # role = session['role']
    # username = session['username']
    # return render_template('index.html', role=role, username=username)
    return render_template("index.html")

@store_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get user input
        username = request.form.get('username')
        password = request.form.get('password')
        # check if user is in db
        user = Person.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id  # Store user ID in session
            session['user_role'] = user.type  # Store user role in session
            flash('You were successfully logged in!')
            return redirect(url_for('store.dashboard'))
        else:
            flash('Invalid username or password!')
            return redirect(url_for('store.login'))
    return render_template("auth.html")

@store_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# @store_bp.route("/logout")
# def logout():
#     return redirect(url_for('store.index'))