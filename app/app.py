from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db, login_manager
from models import User, Task, Challenge
from forms import RegistrationForm, LoginForm, TaskForm, ChallengeForm

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

from models import User, Task, Challenge
from forms import RegistrationForm, LoginForm, TaskForm, ChallengeForm

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email is already registered!', 'danger')
        else:
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new_user = User(email=form.email.data, name=form.name.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))
    else:
        flash('Account NOT created successfully!', 'danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    challenges = Challenge.query.filter_by(created_by=current_user.id).all()
    return render_template('dashboard.html', tasks=tasks, challenges=challenges)

@app.route('/task', methods=['POST'])
@login_required
def task():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(description=form.description.data, user_id=current_user.id)
        current_user.points += 10
        db.session.add(new_task)
        db.session.commit()
        flash('Task completed! You earned 10 points.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/challenge', methods=['POST'])
@login_required
def challenge():
    form = ChallengeForm()
    if form.validate_on_submit():
        if current_user.points >= 1000:
            current_user.points -= 1000
            new_challenge = Challenge(title=form.title.data, description=form.description.data, created_by=current_user.id)
            db.session.add(new_challenge)
            db.session.commit()
            flash('Challenge created successfully!', 'success')
        else:
            flash('You need at least 1000 points to create a challenge.', 'danger')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
