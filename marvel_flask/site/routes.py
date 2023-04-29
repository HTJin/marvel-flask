from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..forms import CharacterForm
from ..models import Character, db
from ..helpers import get_quotes

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    my_character = CharacterForm()
    try:
        if request.method == 'POST' and my_character.validate_on_submit():
            print("Inside POST and validated")
            name = my_character.name.data
            description = my_character.description.data
            comics_appeared_in = my_character.comics.data
            super_power = my_character.power.data
            if my_character.quote.data:
                quote = my_character.quote.data
            else:
                quote = get_quotes(name)
            user_token = current_user.token
            
            character = Character(name, description, comics_appeared_in, super_power, quote, user_token)
            db.session.add(character)
            db.session.commit()
            
            flash(f'{character.__repr__()} 👏', 'character_created ')
            return redirect(url_for('site.profile'))
    except Exception:
        flash('Something was wrong in your entries 😕', 'form-failed')
        raise Exception('Something was wrong in your entries 😕')
    
    current_user_token = current_user.token
    characters = Character.query.filter_by(user_token=current_user_token)
    
    return render_template('profile.html', form=my_character, characters=characters)