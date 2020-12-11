import models

from flask import request, jsonify, Blueprint
from flask_cors import CORS, cross_origin
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from playhouse.shortcuts import model_to_dict


# first argument is blueprints name
# second argument is it's import_name
log = Blueprint('logs', 'log')

@log.route('/', methods=["GET"])
@cross_origin(origin='localhost')
def get_all_logs():
    try:
        logs = [model_to_dict(log) for log in models.UserActivityLog.select()]
        print(logs)
        return jsonify(data=logs, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})