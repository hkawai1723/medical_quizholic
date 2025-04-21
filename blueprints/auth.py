from flask import Blueprint, session, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from flask_dance.contrib.google import google
import string
import random

from form.userform import RegisterForm, LoginForm, ChangePasswordForm
from models.user import User
from extensions import db, login_manager

auth_bp = Blueprint(name='auth', import_name=__name__,
                    template_folder='templates', static_folder='static')


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():  # 自動的にif request.method == 'POST'と同じ条件分岐ができる
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user is None:
            user = User(name=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            session['username'] = username
            session['email'] = email
            flash('Signup is successful!')
        return redirect(url_for('auth.login'))
    return render_template('auth/signup.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Authentication is successful.')
            return redirect(url_for('mainpage.dashboard'))
        else:
            flash('Authentication failed.', 'alert-warning')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/google-login')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))#google loginにリダイレクト
    response = google.get('/oauth2/v2/userinfo')
    username = response.json()['name']
    email = response.json()['email']
    random_password=''.join(random.choices(string.ascii_letters + string.digits, k=16))
    user = User.query.filter_by(email=email).one_or_none()
    if not user:
        user = User(
            name=username,
            email=email,
            auth_provider = 'google'
        )
        user.set_password(random_password)
        db.session.add(user)
        db.session.commit()
    login_user(user, remember=True)
    return redirect(url_for('mainpage.dashboard'))

@auth_bp.route('/logout')
@login_required
def logout():
    if google.authorized:
        token = google.token['access_token']
        response = google.post(
            'https://accounts.google.com/o/oauth2/revoke',
            params={'token': token},
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        print(token)
        print(response)
        if response.ok:
            del google.token
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        new_password = form.new_password.data
        current_user.change_password(new_password)
        flash('Password changed successfully.')
        return redirect(url_for('mainpage.dashboard'))
    return render_template('auth/change_password.html', form=form)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    flash('Login required.', 'alert-warning')
    return redirect('/login')
