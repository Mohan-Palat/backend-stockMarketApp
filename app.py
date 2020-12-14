from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_login import LoginManager 
from flask_httpauth import HTTPBasicAuth
import jwt
from werkzeug.security import generate_password_hash, check_password_hash

DEBUG = True
PORT = 8000

import models

#importing resource
from resources.user import user 
from resources.log import log 

login_manager = LoginManager() # sets up the ability to set up the session

app = Flask(__name__)
###################### added these lines

app.secret_key = "ALFJKSALFKSAKLJASLAKF" ## Need this to encode the session
login_manager.init_app(app) # set up the sessions on the app
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
auth = HTTPBasicAuth()

@login_manager.user_loader # decorator function, that will load the user object whenever we access the session, we can get the user
# by importing current_user from the flask_login
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None
###################### added these lines

@app.before_request
def before_request():
    """Connect to the database before each request"""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """Close the database connection after each request"""
    g.db.close()
    return response

@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})

CORS(user, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(user, url_prefix='/user')

CORS(log, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(log, url_prefix='/logs')
app.config['CORS_HEADERS'] = 'Content-Type'


if __name__ == '__main__':
    print('tables connected')
    models.initialize()
    app.run(debug=DEBUG, port=PORT)