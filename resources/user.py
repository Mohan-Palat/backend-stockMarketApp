import models
from flask_cors import CORS
from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from flask_httpauth import HTTPTokenAuth
from playhouse.shortcuts import model_to_dict


# first argument is blueprints name
# second argument is it's import_name
user = Blueprint('users', 'user')
auth = HTTPTokenAuth(scheme='Bearer')

@user.route('/', methods=["GET"])
def get_all_users():
    try:
        users = [model_to_dict(user) for user in models.User.select()]
        print(users)
        return jsonify(data=users, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})


@user.route('/register', methods=["POST"])
def register():
    ## see request payload anagolous to req.body in express
    ## This is how you get the image you sent over
    ## This has all the data like username, email, password
    payload = request.get_json()
    payload['email'].lower()
    try:
        # Find if the user already exists?
        models.User.get(models.User.email == payload['email']) # model query finding by email
        return jsonify(data={}, status={"code": 401, "message": "A user with that name already exists"})
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password']) # bcrypt line for generating the hash
        user = models.User.create(**payload) # put the user in the database
        activity = models.UserActivityLog.create(username=payload['username'],activityType="user",  activity="A new user has been created")
        # **payload, is spreading like js (...) the properties of the payload object out
        token = user.generate_auth_token().decode('utf-8')
        #login_user
        login_user(user) # starts session
        activity = models.UserActivityLog.create(username=payload['username'],activityType="user", activity="has logged in")
        user_dict = model_to_dict(user)
        print(user_dict)
        print(type(user_dict))
        # delete the password
        del user_dict['password'] # delete the password before we return it, because we don't need the client to be aware of it

        return jsonify(data={"user": user_dict, "token": token}, status={"code": 201, "message": "Success"})

@user.route('/login', methods=["POST"])
def login():
    payload = request.get_json()
    print(payload, '< --- this is playload')
    try:
        user = models.User.get(models.User.username== payload['username']) ### Try find the user by thier email
        user_dict = model_to_dict(user) # if you find the User model convert in to a dictionary so you can access it
        if(check_password_hash(user_dict['password'], payload['password'])): # use bcyrpts check password to see if passwords match
            print(user.generate_auth_token())
            token = user.generate_auth_token().decode('utf-8')
            del user_dict['password'] # delete the password
            login_user(user) # setup the session
            print(user, ' this is user')
            activity = models.UserActivityLog.create(username=payload['username'],activityType="user", activity="has logged in")
            print(current_user.is_authenticated)
            return jsonify(data={"user": user_dict, "token": token}, status={"code": 200, "message": "Success"}) # respond to the client
        else:
            return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})

@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]


@user.route("/logout", methods=["POST"])
def logout():
    payload = request.get_json()
    username = payload['username']
    logout_user()
    activity = models.UserActivityLog.create(username=username,activityType="user", activity="has logged out")
    return 'you have been logged out'