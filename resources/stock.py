import models

from flask import request, jsonify, Blueprint
from flask_cors import CORS, cross_origin
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from playhouse.shortcuts import model_to_dict


# first argument is blueprints name
# second argument is it's import_name
stock = Blueprint('stocks', 'stock')


@stock.route('/create',methods=['POST'])
def add_stock():
        payload = request.get_json()
        print(payload)
        stock = models.Stock.create(user_id=payload['user_id'], watchlist_id=payload['watchlist_id'], stock=payload['stock'])
        # stock = model_to_dict(stock)
        # activity = models.UserActivityLog.create(username=payload['username'], activityType="watchlist", activity="has created a new watchlist")
        return jsonify(data='', status={"code": 201, "message": "Success"})
