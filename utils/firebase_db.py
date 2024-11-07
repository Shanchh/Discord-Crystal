import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import date, datetime, timedelta

class Db_Client:
    def __init__(self):
        cred = credentials.Certificate('setting/discord-crystal-firebase-adminsdk-pwger-2dbef7c56b.json')
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
    
    # 查詢所有訂閱者資料
    def get_all_subscriber_user(self):
        try:
            result = []
            ref = self.db.collection("subscriber_users")
            docs = ref.stream()
            for doc in docs:
                result.append(doc.id)
            return result
        except Exception as e:
            print(f"查詢所有訂閱者時發生錯誤: {e}")
            return False
        
    # 查詢所有訂閱購買資料
    def get_all_detail_lists(self):
        try:
            result = []
            ref = self.db.collection("detail_lists")
            docs = ref.stream()
            for doc in docs:
                result.append(doc.id)
            return result
        except Exception as e:
            print(f"查詢所有訂閱購買資料時發生錯誤: {e}")
            return False

    # 新增訂閱者資料
    def add_subscriber_user(self, userId):
        try:
            ref = self.db.collection("subscriber_users").document(userId)
            ref.set({
                "userId": userId
            })
            return True
        except Exception as e:
            print(f"新增訂閱者時發生錯誤: {e}")
            return False
    
    # 刪除指定訂閱者資料
    def del_subscriber_user(self, userId):
        try:
            ref = self.db.collection("subscriber_users").document(str(userId))
            ref.delete()
            return True
        except Exception as e:
            print(f"刪除訂閱者時發生錯誤: {e}")
            return False
        
    # 新增訂閱資料
    def add_subscriber_detail(self, userId, userName, purchaseDate, quantity, payment):
        try:
            # 確認是否註冊過
            user_doc = self.db.collection("subscriber_users").document(str(userId)).get()
            if not user_doc.exists:
                self.add_subscriber_user(userId)

            dataId = int(datetime.now().timestamp())
            data = {
                "dataId": str(dataId),
                "userId": str(userId),
                "userName": userName,
                "purchaseDate": purchaseDate,
                "quantity": quantity,
                "payment": payment
            }
            ref = self.db.collection("subscriber_users").document(str(userId)).collection("Details").document(str(dataId))
            ref.set(data)
            ref_2 = self.db.collection("detail_lists").document(str(dataId))
            ref_2.set(data)
            return True
        except Exception as e:
            print(f"新增訂閱資料時發生錯誤: {e}")
            return False

    # 列出個人購買明細 
    def list_subscriber_details(self, userId):
        try:
            # 確認是否註冊過
            user_doc = self.db.collection("subscriber_users").document(str(userId)).get()
            if not user_doc.exists:
                return False
            
            ref = self.db.collection("subscriber_users").document(str(userId)).collection("Details")
            docs = ref.stream()
            result = []
            for doc in docs:
                result.append(doc.to_dict())
            return result
        except Exception as e:
            print(f"列出個人購買明細時發生錯誤: {e}")
            return False
        
    # 檢查個人訂閱狀態
    def check_subscriber_state(self, userId):
        try:
            data = self.list_subscriber_details(userId)
            if (data == False):
                return False
            if (len(data) == 1):
                dateDeadLine = self.time_trans(data[0]["purchaseDate"]) + timedelta(days = data[0]["quantity"])
            for index in range(len(data) - 1):
                first_purchaseDate = self.time_trans(data[index]["purchaseDate"])
                second_purchaseDate = self.time_trans(data[index + 1]["purchaseDate"])
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
            return False
    
    # 查詢特定購買明細
    def get_detail(self):
        pass

    # 日期字串轉換系統時間
    def time_trans(self, time):
        return datetime.strptime(time, "%Y/%m/%d")
    
if __name__ == "__main__":
    fb = Db_Client()
    a = fb.check_subscriber_state("123514213412")
    print(a)