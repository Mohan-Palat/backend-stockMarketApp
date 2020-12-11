from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_login import LoginManager 

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

CORS(user, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(user, url_prefix='/user')

CORS(log, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(log, url_prefix='/logs')

if __name__ == '__main__':
    print('tables connected')
    models.initialize()
    app.run(debug=DEBUG, port=PORT)