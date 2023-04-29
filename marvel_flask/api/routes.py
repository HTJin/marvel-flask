from flask import Blueprint, request, jsonify
from ..helpers import token_required, get_quotes, get_images
from ..models import db, Character, character_schema, characters_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/characters', methods=['POST'])
@token_required
def create_character(our_user):
    name = request.json['name']
    super_name = request.json['super_name']
    description = request.json['description']
    comics_appeared_in = request.json['comics_appeared_in']
    super_power = request.json['super_power']
    quote = get_quotes(name, super_name)
    image = get_images(name, super_name)
    user_token = our_user.token
    print(f'User Token: {our_user.token}')
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

@api.route('/characters/<id>', methods=['GET'])
@token_required
def get_character(id):
    if id:
        character = Character.query.get(id)
        response = character_schema.dump(character)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid ID Required'}), 401
 
@api.route('/characters/<id>', methods=['PUT'])
@token_required
def update_character(our_user, id):
    character = Character.query.get(id)
    character.name = request.json['name']
    character.super_name = request.json['super_name']
    character.description = request.json['description']
    character.comics_appeared_in = request.json['comics_appeared_in']
    character.super_power = request.json['super_power']
    character.quote = get_quotes(character.name, character.super_name)
    character.image = get_images(character.name, character.super_name)
    character.user_token = our_user.token
    
    db.session.commit()
    
    response = character_schema.dump(character)
    return jsonify(response)

@api.route('/characters/<id>', methods=['DELETE'])
@token_required
def delete_character(id):
    character = Character.query.get(id)
    
    db.session.delete(character)
    db.session.commit()
    
    response = character_schema.dump(character)
    return jsonify(response)