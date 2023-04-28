from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
@login_required
def profile():
    return render_template('profile.html')