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
    
@monthly_api.route("/get_all_user_data", methods=["GET"])
def get_all_user_data():
    try:
        user_list = monthly.get_all_subscriber_user()
        collection = db["Monthly-Details"]

        discord_ids = [user["discord_id"] for user in user_list]

        aggregation_result = collection.aggregate([
            {"$match": {"discord_id": {"$in": discord_ids}}},
            {"$group": {
                "_id": "$discord_id",
                "total_amount": {"$sum": "$amount"},
                "total_quantity": {"$sum": "$quantity"}
            }}
        ])

        user_totals = {result["_id"]: result for result in aggregation_result}

        for user in user_list:
            discord_id = user["discord_id"]
            user_data = user_totals.get(discord_id, {"total_amount": 0, "total_quantity": 0})
            user["total_amount"] = user_data["total_amount"]
            user["total_quantity"] = user_data["total_quantity"]

        return jsonify({"message": "ok", "data": user_list}), 200
    except Exception as e:
        return jsonify({"Error": str(e)}), 404
    
@monthly_api.route("/get_statistics", methods=["POST"])
def get_statistics():
    try:
        data: dict = request.get_json()
        value = data["value"]
        
        stats = {
            "total_amount": monthly.get_statistics()[0],
            "total_quantity": monthly.get_statistics()[1]
        }

        if value in stats:
            return jsonify({"message": "ok", "data": stats[value]}), 200
        
        return jsonify({"message": "error", "error": "Invalid value."}), 400

    except Exception as e:
        return jsonify({"Error": str(e)}), 404