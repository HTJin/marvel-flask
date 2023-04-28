from flask import request, jsonify, json
from functools import wraps
from .models import User
import secrets, decimal, requests

def token_required(flask_function):
    @wraps(flask_function)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split()[1]
            print(token)
        if not token:
            return jsonify({'message': 'Token is missing'}), 409
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

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default(obj)

def random_joke_generator():
    url = "https://dad-jokes.p.rapidapi.com/random/joke"
    headers = {
        "X-RapidAPI-Key": "b9767d89a9ac296e4893f5c3921076f0",
        "X-RapidAPI-Host": "dad-jokes.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    return data['body'][0]['setup']+' '+data['body'][0]['punchline']