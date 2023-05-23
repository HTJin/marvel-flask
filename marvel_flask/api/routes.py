from flask import Blueprint, request, jsonify, redirect
from ..helpers import token_required, get_quotes, get_images
from ..models import db, Character, character_schema, characters_schema
from ..forms import CharacterForm

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/characters/<fire_token>', methods=['POST'])
@token_required
def create_character(our_user, fire_token):
    name = request.json['name']
    super_name = request.json['super_name']
    description = request.json['description']
    comics_appeared_in = request.json['comics_appeared_in']
    super_power = request.json['super_power']
    quote = get_quotes(name, super_name)
    image = get_images(name, super_name)
    user_token = fire_token
    character = Character(name, super_name, description, comics_appeared_in, super_power, quote, image, user_token=user_token)
    
    db.session.add(character)
    db.session.commit()
    
    response = character_schema.dump(character)
    return jsonify(response)

@api.route('/characters', methods=['GET'])
@token_required
def get_characters(our_user):
    owner = our_user.token
    characters = Character.query.filter_by(user_token=owner).all()
    response = characters_schema.dump(characters)
    return jsonify(response)

@api.route('/characters/<fire_token>', methods=['GET'])
@token_required
def get_character(fire_token):
    owner = fire_token
    character = Character.query.filter_by(user_token=owner).all()
    response = character_schema.dump(character)
    return jsonify(response)
 
@api.route('/characters/<id>/edit', methods=['POST', 'PUT'])
@token_required
def update_character(our_user, id):
    character = Character.query.get(id)

    if not character:
        return jsonify({'message': 'Character not found'}), 404

    form = CharacterForm(request.form)

    if not form.validate():
        return jsonify({'message': 'Invalid form data'}), 400

    character.name = form.name.data
    character.super_name = form.super_name.data
    character.description = form.description.data
    character.comics_appeared_in = form.comics.data
    character.super_power = form.power.data
    character.quote = get_quotes(character.name, character.super_name)
    character.image = get_images(character.name, character.super_name)

    db.session.commit()

    response = character_schema.dump(character)
    return jsonify(response)

@api.route('/characters/<id>/remove', methods=['POST', 'DELETE'])
@token_required
def delete_character(id):
    character = Character.query.get(id)
    
    db.session.delete(character)
    db.session.commit()
    
    character_schema.dump(character)
    return redirect('/profile#character-cards', code=303)