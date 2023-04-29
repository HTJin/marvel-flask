from flask import request, jsonify, json
from functools import wraps
from .models import User
from dotenv import load_dotenv
import secrets, decimal, requests, os


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default(obj)
    
def token_required(flask_function):
    @wraps(flask_function)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split()[1]
            print(token)
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            our_user = User.query.filter_by(token=token).first()
            print(our_user)
            if not our_user or our_user.token != token:
                return jsonify({'message': 'Token is invalid'}), 401
        except:
            our_user = User.query.filter_by(token=token).first()
            if token != our_user.token and secrets.compare_digest(token, our_user.token):
                return jsonify({'message': 'Token is invalid'}), 401
        return flask_function(our_user, *args, **kwargs)
    return decorated

def get_quotes(character_name, character_super_name):
    url = "https://marvel-quote-api.p.rapidapi.com/"
    headers = {
        "content-type": "application/octet-stream",
        "X-RapidAPI-Key": os.getenv('X_RapidAPI_Key'),
        "X-RapidAPI-Host": "marvel-quote-api.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    if character_name.lower() == data['Speaker'] or character_super_name.lower() == data['Speaker']:
        return data['Quote']
    else:
        return data['Quote']+' I heard '+data['Speaker']+' from '+data['Title']+' say that.'

def get_images(character_name, character_super_name):
    response = requests.get(f"https://superheroapi.com/api/{os.getenv('API_KEY')}/search/{character_super_name}")
    data = response.json()
    if data['response'] == 'success':
        for order, entry in enumerate(data['results']):
            if entry['name'].lower() == character_super_name.lower():
                return data['results'][order]['image']['url']
    else: 
        response = requests.get(f"https://superheroapi.com/api/{os.getenv('API_KEY')}/search/{character_name}")
        data = response.json()
        if data['response'] == 'success':
            for order, entry in enumerate(data['results']):
                if entry['name'].lower() == character_name.lower():
                    return data['results'][order]['image']['url']
    return '../static/images/Placeholder_couple_superhero.png'