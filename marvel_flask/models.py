from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow
import uuid, secrets

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    token = db.Column(db.String, default='', unique=True)
    join_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __init__(self, username, email, password):
        self.id = self.set_id()
        self.username = username
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(32)
        
    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        return generate_password_hash(password)
    
    def set_token(self, length):
        return secrets.token_hex(length)
    
    def __repr__(self):
        return f'username: {self.username}, email: {self.email} added to Users'
    
class Character(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(150))
    super_name = db.Column(db.String(150))
    description = db.Column(db.String(1000), nullable=True)
    comics_appeared_in = db.Column(db.Integer)
    super_power = db.Column(db.String)
    quote = db.Column(db.String, nullable=True)
    image = db.Column(db.String, nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)
    
    def __init__(self, name, super_name, description, comics_appeared_in, super_power, quote, image, user_token):
        self.id = self.set_id()
        self.name = name
        self.super_name = super_name
        self.description = description
        self.comics_appeared_in = comics_appeared_in
        self.super_power = super_power
        self.quote = quote
        self.image = image
        self.user_token = user_token
        
    def set_id(self):
        return str(uuid.uuid4())
    
    def __repr__(self):
        return f'{self.name} aka {self.super_name} was added as a Character'
    
class CharacterSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'super_name' 'description', 'comics_appeared_in', 'super_power', 'quote', 'image']
character_schema = CharacterSchema()
characters_schema = CharacterSchema(many=True)