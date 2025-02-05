import time
from bson import ObjectId

from my_utils import time_trans
from datetime import date, datetime, timedelta
from setting.mongodb_setting import db

def get_all_subscriber_user():
    """查詢所有訂閱者資料"""
    try:
        collection = db["Monthly-Users"]
        user_data = list(collection.find())
        user_data = objectid_trans_string(user_data)
        return user_data
    except Exception as e:
        print(f"查詢所有訂閱者時發生錯誤: {e}")
        return False
    
def get_all_detail_lists():
    """查詢所有訂閱購買資料"""
    try:
        collection = db["Monthly-Details"]
        detail_data = list(collection.find())
        detail_data = objectid_trans_string(detail_data)
        return detail_data
    except Exception as e:
        print(f"查詢所有訂閱者時發生錯誤: {e}")
        return False
    
def add_subscriber_user(userId, userName, user_avatar):
    """新增訂閱者資料"""
    try:
        userId = str(userId)
        collection = db["Monthly-Users"]
        
        user = collection.find_one({"discord_id": userId})
        if user: return None

        user_data = {
            "discord_id": userId,
            "discord_name": userName,
            "createAt": int(time.time()),
            "is_active": False,
            "avatar": user_avatar
        }
        collection.insert_one(user_data)
        return True
    except Exception as e:
        print(f"新增訂閱者時發生錯誤: {e}")
        return False
    
def del_subscriber_user(userId):
    """刪除指定訂閱者資料"""
    try:
        userId = str(userId)
        collection = db["Monthly-Users"]

        user = collection.find_one({"discord_id": userId})
        if not user: return None

        collection.delete_one({"_id": user["_id"]})
        return True
    except Exception as e:
        print(f"刪除訂閱者時發生錯誤: {e}")
        return False
    
def add_subscriber_detail(userId, userName, user_avatar, purchaseDate, quantity, payment, amount):
    """新增訂閱資料"""
    try:
        userId = str(userId)
        collection = db["Monthly-Users"]

        user = collection.find_one({"discord_id": userId})
        if not user:
            add_subscriber_user(userId, userName, user_avatar)

        collection = db["Monthly-Details"]
        insert_data = {
            "discord_id": str(userId),
            "discord_name": userName,
            "avatar": user_avatar,
            "createAt": int(datetime.strptime(purchaseDate, "%Y/%m/%d").timestamp()),
            "amount": amount,
            "quantity": quantity,
            "payment": payment
        }
        result = collection.insert_one(insert_data)

        return True, str(result.inserted_id)
    except Exception as e:
        print(f"新增訂閱資料時發生錯誤: {e}")
        return False, ""
    
def del_subscriber_detail(dataId):
    """刪除訂閱資料"""
    try:
        collection = db["Monthly-Details"]

        data = collection.find_one({"_id": ObjectId(dataId)})
        if not data: return None
        
        collection.delete_one({"_id": data["_id"]})
        return True
    except Exception as e:
        print(f"刪除訂閱資料時發生錯誤: {e}")
        return False
    
def list_subscriber_details(userId):
    """列出個人購買明細"""
    try:
        userId = str(userId)
        collection = db["Monthly-Users"]
        
        user = collection.find_one({"discord_id": userId})
        if not user: return None
        
        collection = db["Monthly-Details"]
        user_details = list(collection.find({"discord_id": userId}))

        for detail in user_details:
            detail["_id"] = str(detail["_id"])
            detail["createAt"] = datetime.fromtimestamp(detail["createAt"]).strftime('%Y-%m-%d')
        
        return user_details if user_details else None
    except Exception as e:
        print(f"列出個人購買明細時發生錯誤: {e}")
        return False
    
def get_detail(dataId):
    """查詢特定購買明細"""
    try:
        collection = db["Monthly-Details"]

        data = collection.find_one({"_id": ObjectId(dataId)})

        return data if data else None
    except Exception as e:
        print(f"查詢特定購買明細時發生錯誤: {e}")
        return False

def check_subscriber_state(userId):
    """檢查個人訂閱狀態"""
    try:
        userId = str(userId)
        data = list_subscriber_details(userId)
        if not data:
            return None, None
        if (len(data) == 1):
            dateDeadLine = time_trans(data[0]["createAt"]) + timedelta(days = data[0]["quantity"] * 30)
        for index in range(len(data) - 1):
            first_purchaseDate = time_trans(data[index]["createAt"])
            second_purchaseDate = time_trans(data[index + 1]["createAt"])
            first_quantity = data[index]["quantity"]
            seconde_quantity = data[index + 1]["quantity"]
            # 如果後者開始時間於前者有效期間內
            if (first_purchaseDate + timedelta(days = first_quantity * 30) > second_purchaseDate):
                dateDeadLine = first_purchaseDate + timedelta(days = (first_quantity + seconde_quantity) * 30)
            else:
                dateDeadLine = second_purchaseDate + timedelta(days = seconde_quantity * 30)
        return dateDeadLine.date() > date.today(), dateDeadLine
    except Exception as e:
        print(f"檢查個人訂閱狀態時發生錯誤: {e}")
        return False, None
    
def get_statistics():
    """獲取總統計數據 月數、金額"""
    try:
        collection = db["Monthly-Details"]
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "totalAmount": {"$sum": "$amount"},
                    "totalQuantity": {"$sum": "$quantity"}
                }
            }
        ]
        result = list(collection.aggregate(pipeline))

        total_amount = result[0].get("totalAmount")
        total_quantity = result[0].get("totalQuantity")

        return total_amount, total_quantity
    except Exception as e:
        print(f"獲取總統計數據時發生錯誤: {e}")
        return False, False
    
def get_active_user():
    """列出活躍訂閱者"""
    result = []
    userList = get_all_subscriber_user()
    for user in userList:
        userId = user["discord_id"]
        isActive, dateDeadLine = check_subscriber_state(userId)
        if isActive:
            result.append({
                "userId": userId,
                "dateDeadLine": dateDeadLine
            })
    return result

def refresh_users_active_status(members_with_role):
    """整理資料庫身分組活躍狀態"""
    user_list = get_all_subscriber_user()
    active_ids = [member.id for member in members_with_role]

    collection = db["Monthly-Users"]

    update_count = 0
    for user in user_list:
        user_id = int(user["discord_id"])
        new_status = user_id in active_ids
        if user["is_active"] != new_status:
            collection.update_one(
                {"discord_id": str(user_id)},
                {"$set": {"is_active": new_status}}
            )
            update_count += 1

    return update_count

def objectid_trans_string(data_list):
    for data in data_list:
        data["_id"] = str(data["_id"])
    return data_list

if __name__ == "__main__":
    pass