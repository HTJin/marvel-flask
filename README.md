# Marvel Flask `https://marvel-flask.glitch.me/`

Marvel Flask is a web application built with Flask that allows users to register, log in, create/delete their own characters with quotes and images.

## Features

- User registration and authentication
- Create custom Marvel characters
- Retrieve character quotes and images
- Delete character
- (Edit character tbd)

## Installation and Setup

1. Clone the repository:

git clone https://github.com/HTJin/marvel-flask.git

2. Navigate to the project directory:

`cd marvel-flask`

3. Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate  # For Linux and macOS
venv\Scripts\activate     # For Windows

4. Install the required packages:

`pip install -r requirements.txt`

5. Create a `.env` file in the root directory of the project and add the following environment variables:
```
FLASK_APP=marvel_flask
FLASK_ENV=development
SECRET_KEY=your_secret_key
API_KEY=your_marvel_api_key
DATABASE_URL=your_database_url
```

Replace `your_secret_key` with a secret key of your choice, `your_marvel_api_key` with your Marvel API key, and `your_database_url` with the URL of your database.

6. Run the Flask app:

`flask run`

7. Visit `http://127.0.0.1:5000` in your web browser to view the Marvel Flask app.

## API Used:
1) Marvel-Quote-API - https://rapidapi.com/kyledeguzmanx/api/marvel-quote-api
2) SuperHero API - https://superheroapi.com/

## Usage

1. Register for an account or log in with an existing account.
2. Create your own Marvel character with custom attributes.
3. Retrieve quotes and images for your character.

## Technologies

- Flask
- Jinja2
- SQLAlchemy
- Flask-WTF
- Flask-Login
- Flask-Migrate
- Flask-RESTful
- Flask-Marshmallow
- Flask-CORS
- Tailwind CSS
