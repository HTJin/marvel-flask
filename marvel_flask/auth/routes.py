from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..forms import LoginForm, RegisterForm
from ..models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            user = User(username, email, password=password)
            db.session.add(user)
            db.session.commit()
            flash(f'{user.__repr__()}', 'user_created')
            return redirect(url_for('auth.login'))
    except:
        raise Exception('Something was wrong in your entries 😕')
    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user_current = User.query.filter(User.email == email).first()
            if user_current and check_password_hash(user_current.password, password):
                flash(f'Hello {user_current.username}, you are logged in!', 'auth-success')
                login_user(user_current)
                print(f'Redirecting to your profile! 😎')
                return redirect(url_for('site.profile'))
            else:
                flash(f'Hmm your email/password was incorrect', 'auth-failed')
                print(f'Redirecting back to Login! 🔑')
                return redirect(url_for('auth.login'))
    except:
        flash('Something was wrong in your entries 😕', 'form-failed')
        raise Exception('Something was wrong in your entries 😕')
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(f'You have successfully logged out! 👌', 'logged-out')
    print(f'You have successfully logged out! 👌')
    return redirect(url_for('site.home'))