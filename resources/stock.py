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
        stock = model_to_dict(stock)
        activity = models.UserActivityLog.create(username=payload['username'], activityType="watchlist", activity="has added a stock to their watchlist")
        return jsonify(data=stock, status={"code": 201, "message": "Success"})

@stock.route('/watchlist',methods=['POST'])
def get_watchlist_stocks():
    payload = request.get_json()
    stocks = [model_to_dict(stock) for stock in models.Stock.select(models.Stock.stock,models.Stock.id,models.Stock.user, models.Stock.watchlist).join(models.Watchlist).where(models.Watchlist.watchlistname == payload['watchlistname'])]
    return jsonify(data=stocks, status={"code": 201, "message": "Success"})
