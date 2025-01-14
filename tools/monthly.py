from utils.firebase_db import Db_Client
from datetime import date, datetime, timedelta

def check_subscriber_state(userId):
    """檢查個人訂閱狀態"""
    try:
        db = Db_Client()
        data = db.list_subscriber_details(userId)
        if (data == False):
            return False
        if (len(data) == 1):
            dateDeadLine = time_trans(data[0]["purchaseDate"]) + timedelta(days = data[0]["quantity"] * 30)
        for index in range(len(data) - 1):
            first_purchaseDate = time_trans(data[index]["purchaseDate"])
            second_purchaseDate = time_trans(data[index + 1]["purchaseDate"])
            first_quantity = data[index]["quantity"]
            seconde_quantity = data[index + 1]["quantity"]
            # 如果後者開始時間於前者有效期間內
            if (first_purchaseDate + timedelta(days = first_quantity * 30) > second_purchaseDate):
                dateDeadLine = first_purchaseDate + timedelta(days = (first_quantity + seconde_quantity) * 30)
            else:
                dateDeadLine = second_purchaseDate + timedelta(days = seconde_quantity * 30)
        return True, dateDeadLine if dateDeadLine.date() > date.today() else False
    except Exception as e:
        print(f"檢查個人訂閱狀態時發生錯誤: {e}")
        return False, None

def time_trans(time):
    """日期字串轉換系統時間"""
    return datetime.strptime(time, "%Y/%m/%d")

if __name__ == "__main__":
    pass