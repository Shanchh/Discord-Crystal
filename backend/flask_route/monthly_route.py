from flask import jsonify, Blueprint

import common.monthly as monthly

monthly_api = Blueprint("monthly_api", __name__)

@monthly_api.route("/get_all_subscriber_user", methods=["GET"])
def get_all_subscriber_user():
    try:
        user_list = monthly.get_all_subscriber_user()
        result = {
            "message": "ok",
            "data": user_list
        }
        return result

    except Exception as e:
        return jsonify({"Error": str(e)}), 404
    
@monthly_api.route("/get_all_detail_lists", methods=["GET"])
def get_all_detail_lists():
    try:
        detail_list = monthly.get_all_detail_lists()
        result = {
            "message": "ok",
            "data": detail_list[::-1]
        }
        return result

    except Exception as e:
        return jsonify({"Error": str(e)}), 404