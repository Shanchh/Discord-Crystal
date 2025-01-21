from flask import jsonify, Blueprint, request
from datetime import datetime
from bson import ObjectId

from setting.mongodb_setting import db
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
    
@monthly_api.route("/modify_detail", methods=["POST"])
def modify_detail():
    try:
        data: dict = request.get_json()
        values = data["values"]
        query = {"_id": ObjectId(values["_id"])}
        update = {
            "$set": {
                "discord_name": values["name"],
                "createAt": int(datetime.strptime(values["createTime"], "%Y-%m-%d").timestamp()),
                "amount": int(values["amount"]),
                "quantity": int(values["quantity"]),
                "payment": values["payment"]
            }
        }
        modify_result = db["Monthly-Details"].update_one(query, update)
        result = {
            "message": "ok",
            "modify": modify_result.modified_count
        }
        return result

    except Exception as e:
        return jsonify({"Error": str(e)}), 404
    
@monthly_api.route("/delete_detail", methods=["POST"])
def delete_detail():
    try:
        data: dict = request.get_json()
        id = data["id"]

        collection = db["Monthly-Details"]
        detail = collection.find_one({"_id": ObjectId(id)})

        if not detail:
            return jsonify({"message": "NotFound"}), 404
        
        collection.delete_one({"_id": ObjectId(id)})

        result = {
            'code': 0,
            'message': f"成功刪除帳號"
        }

        return result

    except Exception as e:
        return jsonify({"Error": str(e)}), 404