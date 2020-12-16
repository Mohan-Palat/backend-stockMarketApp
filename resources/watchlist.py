import models

from flask import request, jsonify, Blueprint
from flask_cors import CORS, cross_origin
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from playhouse.shortcuts import model_to_dict


# first argument is blueprints name
# second argument is it's import_name
watchlist = Blueprint('watchlists', 'watchlist')

@watchlist.route('/', methods=["GET"])
def get_all_watchlists():
    try:
        watchlists = [model_to_dict(watchlist) for watchlist in models.Watchlist
                                                .select()]
        print(watchlists)
        return jsonify(data=watchlists, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@watchlist.route('/<id>', methods=["GET"])
def get_user_watchlists(id):
    try:
        print(id)
        watchlists = [model_to_dict(watchlist) for watchlist in models.Watchlist
                                                .select().where(models.Watchlist.watchlist_id == id)
                                                .order_by(models.Watchlist.created_at.desc())]
        return jsonify(data=watchlists, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@watchlist.route('/create',methods=['POST'])
def create_watchlist():
    payload = request.get_json()
    watchlist = models.Watchlist.create(watchlist_id=payload['watchlist_id'], watchlistname=payload['watchlistname'])
    watchlist = model_to_dict(watchlist)
    activity = models.UserActivityLog.create(username=payload['username'], activityType="watchlist", activity="has created a new watchlist")
    return jsonify(data=watchlist, status={"code": 201, "message": "Success"})
